from django.contrib import admin
from django.urls import path
from video import views as video_view
from gpo import views as gpo_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Django admin
    path("admin/", admin.site.urls),
    # User management
    path("login/", gpo_view.login_view, name="login"),
    path("logout/", gpo_view.logout_view, name="logout"),
    # Local apps
    path("", gpo_view.main_view, name="main-view"),
    path("channel/", gpo_view.channel_view, name="channel-view"),
    path("single-channel/<group_slug>/", gpo_view.single_channel_view, name="single-channel-view"),
    # Video
    path("video/<slug:video_slug>/", video_view.single_video_view, name="single-video"),
    path("serve-hls-playlist/<int:video_id>/", video_view.serve_hls_playlist, name="serve_hls_playlist"),
    path("serve_hls_segment/<int:video_id>/<str:segment_name>/", video_view.serve_hls_segment, name="serve_hls_segment"),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
