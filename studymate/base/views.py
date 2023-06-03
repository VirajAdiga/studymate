from django.db.models import Q
from django.shortcuts import render, redirect

from base.forms import RoomForm
from base.models import Room, Topic


def home(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ""
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    room_count = rooms.count()
    topics = Topic.objects.all()
    return render(request, "base/home.html", {"rooms": rooms, "topics": topics, "room_count": room_count})


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


def update_room(request, pk):
    required_room = Room.objects.get(id=pk)
    form = RoomForm(instance=required_room)
    if request.method == "POST":
        form = RoomForm(request.POST, instance=required_room)
        if form.is_valid():
            form.save()
            return redirect("home")
    return render(request, "base/create_room.html", {"form": form})


def delete_room(request, pk):
    required_room = Room.objects.get(id=pk)
    if request.method == "POST":
        required_room.delete()
        return redirect("home")
    return render(request, "base/delete.html", {"obj": required_room})
