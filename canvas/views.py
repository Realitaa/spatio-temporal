from django.http import JsonResponse
from .services import create_canvas_with_video


def upload_video(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    file = request.FILES.get('video')

    if not file:
        return JsonResponse({'error': 'No file uploaded'}, status=400)

    result = create_canvas_with_video(file)

    canvas = result["canvas"]
    video = result["video"]

    return JsonResponse({
        "canvas_id": canvas.id,
        "video_id": video.id,
        "video_url": video.file.url
    })