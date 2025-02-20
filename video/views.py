import os
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.http import FileResponse, HttpResponse
from .models import Video
from django.contrib.auth.decorators import login_required
from gpo.models import Group

@login_required
def serve_hls_playlist(request, video_id):
    try:
        video = get_object_or_404(Video, pk=video_id)
        hls_playlist_path = video.hls

        with open(hls_playlist_path, 'r') as m3u8_file:
            m3u8_content = m3u8_file.read()

        base_url = request.build_absolute_uri('/')
        serve_hls_segment_url = base_url + "serve_hls_segment/" + str(video_id)
        m3u8_content = m3u8_content.replace('{{ dynamic_path }}', serve_hls_segment_url)
        
        return HttpResponse(m3u8_content, content_type='application/vnd.apple/mpegurl')
    except (Video.DoesNotExist, FileNotFoundError):
        return HttpResponse("Video or HLS playlist not found", status=404)

@login_required   
def serve_hls_segment(request, video_id, segment_name):
    try:
        video = get_object_or_404(Video, pk=video_id)
        hls_directory = os.path.join(os.path.dirname(video.video_file.path), f'hls_output_{video.slug}')
        segment_path = os.path.join(hls_directory, segment_name)

        # Read HLS segment as a binary:
        return FileResponse(open(segment_path, 'rb'))
    except (Video.DoesNotExist, FileNotFoundError):
        return HttpResponse("Video or HLS segment not found", status=404)

@login_required
def single_video_view(request, video_slug):
    try:
        video = Video.objects.get(slug=video_slug)  # Sử dụng get() thay vì filter()
        user = request.user
        groups = Group.objects.filter(member=user)
        videos = []
        for group in groups:
            videos.extend(group.video.all().order_by("-id"))

        hls_playlist_url = reverse("serve_hls_playlist", args=[video.id])  # Sử dụng reverse để tạo URL

        context = {
            "hls_url": hls_playlist_url,
            "video": video,
            "groups": groups,
            "videos": videos,
        }

        return render(request, "video-page.html", context)

    except Video.DoesNotExist:
        return HttpResponse("Video not found", status=404)