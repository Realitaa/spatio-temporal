import cv2
import uuid
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