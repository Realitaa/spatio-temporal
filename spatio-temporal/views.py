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

        # Fetch analysis result if it exists
        try:
            analysis_obj = canvas_obj.analysis
            analysis_result = {
                "summary": {
                    "duration": analysis_obj.duration,
                    "fps": video.fps,
                    "total_activity": analysis_obj.total_integral,
                    "average": analysis_obj.average_activity,
                    "max": analysis_obj.max_activity,
                    "min": analysis_obj.min_activity,
                    "peak_time": analysis_obj.peak_time,
                },
                "graph": analysis_obj.graph_data,
                "heatmap": analysis_obj.heatmap,
            }
        except Exception: # AnalysisResult.DoesNotExist
            analysis_result = None

    except Canvas.DoesNotExist:
        canvas_name = ""
        has_roi = False
        video = None
        analysis_result = None

    return render(
        request,
        "Analysis",
        {
            "video_id": video_id,
            "video_url": video.file.url if video and video.file else None,
            "canvas_id": canvas_obj.id if canvas_obj else None,
            "canvas_name": canvas_name,
            "has_roi": has_roi,
            "thumbnail_url": video.thumbnail.url if video and video.thumbnail else None,
            "original_width": video.width if video else None,
            "original_height": video.height if video else None,
            "analysis_result": analysis_result,
        },
    )
