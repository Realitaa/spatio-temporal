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
        has_roi = canvas_obj.has_roi()
        video = canvas_obj.video
    except Canvas.DoesNotExist:
        canvas_name = ""
        has_roi = False
        video = None

    return render(
        request,
        "Analysis",
        {
            "video_id": video_id,
            "canvas_id": canvas_obj.id if canvas_obj else None,
            "canvas_name": canvas_name,
            "has_roi": has_roi,
            "thumbnail_url": video.thumbnail.url if video and video.thumbnail else None,
            "original_width": video.width if video else None,
            "original_height": video.height if video else None,
        },
    )
