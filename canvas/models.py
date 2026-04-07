from django.db import models
from django.contrib.auth.models import User

class Canvas(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Video(models.Model):
    canvas = models.OneToOneField(Canvas, on_delete=models.CASCADE, related_name='video')

    file = models.FileField(upload_to='uploads/')
    
    duration = models.FloatField(null=True, blank=True)  # detik
    total_frames = models.IntegerField(null=True, blank=True)

    status = models.CharField(max_length=20, default='uploaded')
    progress = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

class AnalysisResult(models.Model):
    canvas = models.OneToOneField(Canvas, on_delete=models.CASCADE, related_name='analysis')

    # Ringkasan
    duration = models.FloatField()
    total_frames = models.IntegerField()
    average_activity = models.FloatField()

    # Aktivitas
    max_activity = models.FloatField()
    max_time = models.FloatField()
    min_activity = models.FloatField()
    peak_start = models.FloatField()
    peak_end = models.FloatField()

    # Integral
    total_integral = models.FloatField()
    method = models.CharField(max_length=50, default='Riemann Sum')