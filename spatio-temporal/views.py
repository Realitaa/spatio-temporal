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
    except Canvas.DoesNotExist:
        canvas_name = ""

    return render(
        request,
        "Analysis",
        {
            "video_id": video_id,
            "canvas_name": canvas_name,
        },
    )
