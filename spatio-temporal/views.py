from inertia import render


def home(request):
    return render(request, "Index")

def about(request):
    return render(request, "About")