from inertia import render

from canvas.models import Canvas


def home(request):
    return render(request, "Index")


def about(request):
    return render(request, "About")


def canvas(request):
    return render(request, "Canvas")


def analysis(request, video_id):
    try:
        canvas_obj = Canvas.objects.get(id=video_id)
        canvas_name = canvas_obj.name
        has_roi = all(
            v is not None for v in [
                canvas_obj.roi_x1,
                canvas_obj.roi_y1,
                canvas_obj.roi_x2,
                canvas_obj.roi_y2
            ]
        )
    except Canvas.DoesNotExist:
        canvas_name = ""
        has_roi = False

    return render(
        request,
        "Analysis",
        {
            "video_id": video_id,
            "canvas_name": canvas_name,
            "has_roi": has_roi,
            "thumbnail_url": canvas_obj.video.thumbnail.url if canvas_obj.video.thumbnail else None
        },
    )
