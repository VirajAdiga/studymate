from django.shortcuts import render

from base.models import Room


def home(request):
    return render(request, "base/home.html")


def rooms(request):
    context = {"rooms": Room.objects.all()}
    return render(request, "base/rooms.html", context)


def room(request, pk):
    room_requested = Room.objects.get(id=int(pk))
    context = {"room": room_requested}
    return render(request, "base/room.html", context)
