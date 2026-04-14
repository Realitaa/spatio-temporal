import cv2
import uuid
import numpy as np
from django.core.files.base import ContentFile
from .models import Canvas, Video


def create_canvas_with_video(file):
    # 1. buat canvas
    canvas = Canvas.objects.create(name=f"Canvas Baru {Canvas.objects.count() + 1}")

    # 2. attach video
    video = Video.objects.create(canvas=canvas, file=file, status="uploaded")

    generate_thumbnail(video)

    return {"canvas": canvas, "video": video}

def generate_thumbnail(video):
    cap = cv2.VideoCapture(video.file.path)

    if not cap.isOpened():
        return

    # Extract video dimensions
    video.width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    video.height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    ret, frame = cap.read()

    if ret:
        # encode ke jpg
        _, buffer = cv2.imencode(".jpg", frame)

        file_name = f"{uuid.uuid4().hex}.jpg"

        # simpan ke ImageField Django
        video.thumbnail.save(
            file_name,
            ContentFile(buffer.tobytes()),
            save=False
        )

    cap.release()

    video.save()

def process_video(canvas_id):
    canvas = Canvas.objects.get(id=canvas_id)
    video = canvas.video

    # ===== ROI (original scale) =====
    x1, y1, x2, y2 = (
        canvas.roi_x1,
        canvas.roi_y1,
        canvas.roi_x2,
        canvas.roi_y2,
    )

    # ===== Video =====
    cap = cv2.VideoCapture(video.file.path)

    if not cap.isOpened():
        raise Exception("Gagal membuka video")

    fps = cap.get(cv2.CAP_PROP_FPS)

    # ===== PARAMETER =====
    frame_skip = 5
    rows, cols = 5, 5

    TARGET_W, TARGET_H = 640, 360

    # ===== SCALE ROI =====
    scale_x = TARGET_W / video.width
    scale_y = TARGET_H / video.height

    rx1 = int(x1 * scale_x)
    ry1 = int(y1 * scale_y)
    rx2 = int(x2 * scale_x)
    ry2 = int(y2 * scale_y)

    # ===== INIT =====
    prev_gray = None
    frame_count = 0

    total_grid = np.zeros((rows, cols))
    frame_used = 0
    activity_over_time = []

    # ===== MAIN LOOP =====
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1

        if frame_count % frame_skip != 0:
            continue

        frame = cv2.resize(frame, (TARGET_W, TARGET_H))
        roi = frame[ry1:ry2, rx1:rx2]

        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

        if prev_gray is None:
            prev_gray = gray
            continue

        diff = cv2.absdiff(prev_gray, gray)
        _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)

        prev_gray = gray

        h, w = thresh.shape
        cell_h = h // rows
        cell_w = w // cols

        grid = np.zeros((rows, cols))

        for i in range(rows):
            for j in range(cols):
                cell = thresh[
                    i*cell_h:(i+1)*cell_h,
                    j*cell_w:(j+1)*cell_w
                ]

                activity = np.sum(cell) / 255
                grid[i][j] = activity

        total_grid += grid
        frame_used += 1

        frame_activity = np.sum(grid)
        activity_over_time.append(frame_activity)

    cap.release()

    # ===== POST PROCESS =====
    normalized_grid = total_grid / frame_used if frame_used else total_grid
    real_total = float(np.sum(activity_over_time))

    time_per_point = frame_skip / fps if fps else 0
    time_series = [i * time_per_point for i in range(len(activity_over_time))]

    max_val = float(np.max(activity_over_time)) if activity_over_time else 0
    min_val = float(np.min(activity_over_time)) if activity_over_time else 0
    avg_val = float(np.mean(activity_over_time)) if activity_over_time else 0

    peak_index = int(np.argmax(activity_over_time)) if activity_over_time else 0
    peak_time = peak_index * time_per_point

    duration = len(activity_over_time) * time_per_point

    # ===== RESULT =====
    result = {
        "summary": {
            "duration": float(duration),
            "total_activity": real_total,
            "average": avg_val,
            "max": max_val,
            "min": min_val,
            "peak_time": float(peak_time)
        },
        "graph": {
            "time": time_series,
            "activity": [float(x) for x in activity_over_time]
        },
        "heatmap": normalized_grid.tolist()
    }

    # Save to Database
    from .models import AnalysisResult
    AnalysisResult.objects.update_or_create(
        canvas=canvas,
        defaults={
            "duration": float(duration),
            "total_frames": frame_used,
            "average_activity": avg_val,
            "max_activity": max_val,
            "min_activity": min_val,
            "peak_time": float(peak_time),
            "total_integral": real_total,
            "graph_data": result["graph"],
            "heatmap": result["heatmap"],
        }
    )

    return result