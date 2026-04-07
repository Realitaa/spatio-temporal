from django.urls import path
from . import views

app_name = "canvas"

urlpatterns = [
    path("upload/", views.upload_video, name="upload_video"),
]