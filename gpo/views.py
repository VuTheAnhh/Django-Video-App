from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from video.models import Video
from .models import Group

def login_view(request):
    if request.method == "POST":

        username = request.POST.get("account")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            if user.is_active: 
                login(request, user)
                return redirect("/")  
            else:
                error_message = "Your account is inactive."
        else:
            error_message = "Invalid account or password"
        
        return render(request, "login.html", {"error_message": error_message})
    else:
        return render(request, "login.html")

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def main_view(request):
    user = request.user
    groups = Group.objects.filter(member=user)
    videos = []
    for group in groups:
        videos.extend(group.video.all().order_by("id"))

    videos = list(set(videos))

    context = {
        "groups": groups,
        "videos": videos,
    }

    return render(request, "index.html", context)

@login_required
def channel_view(request):
    user = request.user
    groups = Group.objects.filter(member=user)
    videos = []

    for group in groups:
        videos.extend(group.video.all())

    context = {
        "groups": groups,
        "videos": videos,
    }

    return render(request, "channel.html", context)

def single_channel_view(request, group_slug):
    group = Group.objects.get(slug=group_slug)
    videos = group.video

    context = {
        "group": group,
        "videos": videos,
    }

    return render(request, "single-channel.html", context)
