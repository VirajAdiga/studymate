from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect

from base.forms import RoomForm
from base.models import Room, Topic


def register(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "An error occurred while registration")
    return render(request, "base/register.html", {"form": form})


def login_page(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username, password=password)
        except User.DoesNotExist:
            messages.error(request, "Invalid credentials")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("home")

    return render(request, "base/login.html")


def logout_page(request):
    logout(request)
    return redirect("home")


def home(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ""
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    ).select_related("topic", "host")

    room_count = rooms.count()
    topics = Topic.objects.all()
    return render(request, "base/home.html", {"rooms": rooms, "topics": topics, "room_count": room_count})


@login_required(login_url="login")
def create_room(request):
    form = RoomForm()
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    return render(request, "base/create_room.html", {"form": form})


def get_room(request, pk):
    room_requested = Room.objects.get(id=int(pk))
    context = {"room": room_requested}
    return render(request, "base/room.html", context)


@login_required(login_url="login")
def update_room(request, pk):
    required_room = Room.objects.get(id=pk)
    form = RoomForm(instance=required_room)

    if request.user != required_room.host and not (request.user.is_staff or request.user.is_super_user):
        return HttpResponse("Forbidden")

    if request.method == "POST":
        form = RoomForm(request.POST, instance=required_room)
        if form.is_valid():
            form.save()
            return redirect("home")
    return render(request, "base/create_room.html", {"form": form})


@login_required(login_url="login")
def delete_room(request, pk):
    required_room = Room.objects.get(id=pk)

    if request.user != required_room.host and not (request.user.is_staff or request.user.is_super_user):
        return HttpResponse("Forbidden")

    if request.method == "POST":
        required_room.delete()
        return redirect("home")
    return render(request, "base/delete.html", {"obj": required_room})
