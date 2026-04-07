from .models import Canvas, Video


def create_canvas_with_video(file):
    # 1. buat canvas
    canvas = Canvas.objects.create(name=f"Canvas Baru {Canvas.objects.count() + 1}")

    # 2. attach video
    video = Video.objects.create(canvas=canvas, file=file, status="uploaded")

    return {"canvas": canvas, "video": video}
