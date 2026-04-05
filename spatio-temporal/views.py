from inertia import render


def home(request):
    return render(request, "Index")

def about(request):
    return render(request, "About")

def canvas(request):
    return render(request, "Canvas")

def analysis(request, video_id):
    return render(request, "Analysis", {
        "video_id": video_id
    })