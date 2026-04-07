from django.http import JsonResponse

from .models import Canvas
from .services import create_canvas_with_video


def list_canvases(request):
    if request.method != "GET":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    canvases = Canvas.objects.order_by("-created_at").values("id", "name", "created_at")
    return JsonResponse({"canvases": list(canvases)})


def upload_video(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    file = request.FILES.get("video")

    if not file:
        return JsonResponse({"error": "No file uploaded"}, status=400)

    result = create_canvas_with_video(file)

    canvas = result["canvas"]
    video = result["video"]

    return JsonResponse(
        {"canvas_id": canvas.id, "video_id": video.id, "video_url": video.file.url}
    )
