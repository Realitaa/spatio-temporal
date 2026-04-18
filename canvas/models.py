import os
import uuid

from django.db import models


def random_video_filename(instance, filename):
    ext = os.path.splitext(filename)[1]
    return f"uploads/videos/{uuid.uuid4().hex}{ext}"

def random_thumbnails_filename(instance, filename):
    ext = os.path.splitext(filename)[1]
    return f"uploads/thumbnails/{uuid.uuid4().hex}{ext}"


class Canvas(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    # ROI (dalam koordinat ORIGINAL video)
    roi_x1 = models.IntegerField(null=True, blank=True)
    roi_y1 = models.IntegerField(null=True, blank=True)
    roi_x2 = models.IntegerField(null=True, blank=True)
    roi_y2 = models.IntegerField(null=True, blank=True)


    def __str__(self):
        return self.name
    
    def has_roi(self):
        return all([
            self.roi_x1 is not None,
            self.roi_y1 is not None,
            self.roi_x2 is not None,
            self.roi_y2 is not None,
        ])


class Video(models.Model):
    canvas = models.OneToOneField(
        Canvas, on_delete=models.CASCADE, related_name="video"
    )

    file = models.FileField(upload_to=random_video_filename, blank=True)
    thumbnail = models.ImageField(upload_to=random_thumbnails_filename, null=True, blank=True)

    fps = models.FloatField(null=True, blank=True)
    duration = models.FloatField(null=True, blank=True)  # detik
    total_frames = models.IntegerField(null=True, blank=True)

    status = models.CharField(max_length=20, default="uploaded")
    progress = models.IntegerField(default=0)

    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)


class AnalysisResult(models.Model):
    canvas = models.OneToOneField(
        Canvas, on_delete=models.CASCADE, related_name="analysis"
    )

    # Ringkasan
    duration = models.FloatField()
    total_frames = models.IntegerField(null=True, blank=True)
    average_activity = models.FloatField()

    # Aktivitas
    max_activity = models.FloatField()
    max_time = models.FloatField(null=True, blank=True)
    min_activity = models.FloatField()
    peak_time = models.FloatField(null=True, blank=True)
    peak_start = models.FloatField(null=True, blank=True)
    peak_end = models.FloatField(null=True, blank=True)

    # Integral
    total_integral = models.FloatField()
    method = models.CharField(max_length=50, default="Riemann Sum")

    # JSON Data for graph and heatmap
    graph_data = models.JSONField(null=True, blank=True)
    heatmap = models.JSONField(null=True, blank=True)
