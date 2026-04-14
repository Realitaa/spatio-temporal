import json

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from .models import Canvas
from .services import create_canvas_with_video


@require_http_methods(["GET"])
def list_canvases(request):
    canvases = Canvas.objects.order_by("-created_at").values("id", "name", "created_at")
    return JsonResponse({"canvases": list(canvases)})


@require_http_methods(["PATCH"])
def rename_canvas(request, canvas_id):
    try:
        canvas = Canvas.objects.get(id=canvas_id)
    except Canvas.DoesNotExist:
        return JsonResponse({"error": "Canvas not found"}, status=404)

    try:
        body = json.loads(request.body)
        name = body.get("name", "").strip()
    except (json.JSONDecodeError, AttributeError):
        return JsonResponse({"error": "Invalid JSON body"}, status=400)

    if not name:
        return JsonResponse({"error": "Name cannot be empty"}, status=400)

    canvas.name = name
    canvas.save(update_fields=["name"])

    return JsonResponse({"id": canvas.id, "name": canvas.name})


@require_http_methods(["POST"])
def upload_video(request):
    file = request.FILES.get("video")

    if not file:
        return JsonResponse({"error": "No file uploaded"}, status=400)

    result = create_canvas_with_video(file)

    canvas = result["canvas"]
    video = result["video"]

    return JsonResponse({
        "canvas_id": canvas.id,
        "video_id": video.id,
        "video_url": video.file.url,
        "thumbnail_url": video.thumbnail.url if video.thumbnail else None
    })


@require_http_methods(["DELETE"])
def delete_canvas(request, canvas_id):
    try:
        canvas = Canvas.objects.get(id=canvas_id)
    except Canvas.DoesNotExist:
        return JsonResponse({"error": "Canvas not found"}, status=404)

    canvas.delete()
    return JsonResponse({"message": "Canvas deleted successfully"})
