from django.db import models
from django.contrib.auth.models import User

class Canvas(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="canvases")
    title = models.CharField(max_length=255, default="Kanvas Baru")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Video(models.Model):
    canvas = models.OneToOneField(Canvas, on_delete=models.CASCADE, related_name="video")
    file = models.FileField(upload_to="videos/")
    duration = models.FloatField(null=True, blank=True)
    fps = models.FloatField(null=True, blank=True)
    total_frames = models.IntegerField(null=True, blank=True)

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Video for {self.canvas.title}"

class FrameAnalysis(models.Model):
    canvas = models.ForeignKey(Canvas, on_delete=models.CASCADE, related_name="frames")

    frame_index = models.IntegerField()
    timestamp = models.FloatField()  # detik

    # contoh data (bebas sesuai project kamu)
    object_count = models.IntegerField(null=True, blank=True)
    motion_value = models.FloatField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["frame_index"]

class Insight(models.Model):
    canvas = models.OneToOneField(Canvas, on_delete=models.CASCADE, related_name="insight")

    summary = models.TextField(blank=True)
    max_object = models.IntegerField(null=True, blank=True)
    avg_motion = models.FloatField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)