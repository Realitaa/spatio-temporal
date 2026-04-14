from django.urls import path

from . import views

app_name = "canvas"

urlpatterns = [
    path("", views.list_canvases, name="list_canvases"),
    path("<int:canvas_id>/rename/", views.rename_canvas, name="rename_canvas"),
    path("upload/", views.upload_video, name="upload_video"),
    path("<int:canvas_id>/delete/", views.delete_canvas, name="delete_canvas"),
    path("<int:canvas_id>/set-roi/", views.set_roi, name="set_roi"),
]
