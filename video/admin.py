from django.contrib import admin
from .models import Video

class VideoAdmin(admin.ModelAdmin):
    lst = [
        "video_name",
        "deep_encode",
        "created_at",
        "updated_at",
        "duration",
        "status",
        "is_running",
    ]
    
    list_display = lst
    search_fields = lst

admin.site.register(Video, VideoAdmin)