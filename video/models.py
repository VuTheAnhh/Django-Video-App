import os
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.db.models.signals import post_save, pre_delete
from .formater import video_encode
import shutil

def validate_mp4_extension(value):
    ext = os.path.splitext(value.name)[1] # == ".mp4"

    if ext.lower() != ".mp4":
        raise ValidationError("Only .mp4 files are allowed.")
    
def validate_video_name(value):
    name = os.path.splitext(value.name)[0]

    if len(name) >= 20:
        new_name = name[:20] + ".mp4"
        value.name = new_name

class Video(models.Model):
    PENDING = "Pending"
    PROCESSING = "Processing"
    COMPLETED = "Completed"

    STATUS_CHOICES = (
        (PENDING, "Pending"),
        (PROCESSING, "Processing"),
        (COMPLETED, "Completed"),
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    video_name = models.CharField(max_length=500, help_text=("Please enter video's name"))
    deep_encode = models.BooleanField(default=False, help_text=("Check if video need to encode"))
    slug = models.SlugField(max_length=500, unique=True, null=True, blank=True, help_text=("Leave this field blank, it will automatically generated"))
    description = models.TextField(null=True, blank=True, help_text=("Please provide some information about your video (You can leave this field blank)"))
    video_file = models.FileField(upload_to="videos", validators=[validate_mp4_extension, validate_video_name], help_text=("Please select the video"))
    thumbnail = models.ImageField(upload_to="thumbnails", null=True, blank=True, help_text=("Leave this field blank, it will automatically generated"))
    duration = models.CharField(max_length=20, blank=True, null=True, help_text=("Leave this field blank, it will automatically generated"))
    hls = models.CharField(max_length=500, blank=True, null=True, help_text=("Leave this field blank, it will automatically generated"))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING, help_text=("Leave this field, it is automatic"))
    is_running = models.BooleanField(default=False, help_text=("Leave this field, it is automatic"))

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.video_name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.video_name)
        super().save(*args, **kwargs)

def invoke_video_encode(sender, instance, created, *args, **kwargs):
    if created:
        video_encode(instance=instance)
        print("__________________ Completed __________________")
    else:
        pass

def delete_video(sender, instance, using, **kwargs):
    video_file_path = instance.video_file.path
    correct_video_file_path = os.path.normpath(video_file_path)
    
    hls_file_path = instance.hls
    hls_dir_path = os.path.dirname(hls_file_path)

    if os.path.isfile(correct_video_file_path):
        os.remove(correct_video_file_path)

    if os.path.isdir(hls_dir_path):
        shutil.rmtree(hls_dir_path)


post_save.connect(invoke_video_encode, sender=Video)
pre_delete.connect(delete_video, sender=Video)
        