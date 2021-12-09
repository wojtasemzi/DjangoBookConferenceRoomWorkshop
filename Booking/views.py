from datetime import date
from django.http.response import HttpResponse
from django.shortcuts import redirect, render

from django.views import View
from django.core.exceptions import ObjectDoesNotExist

from Booking import models

class AddRoom(View):
    def get(self, request) -> HttpResponse:
        return render(request, 'add_room.html')

    def post(self, request) -> HttpResponse:
        name = request.POST.get('name')
        if name == '':
            return render(request, 'add_room.html', {'error': 'Musisz podać nazwę sali konferencyjnej.'})
        try:
            rooms = models.Rooms.objects.get(name__iexact=name)
            return render(request, 'add_room.html', {'error': 'Musisz podać unikatową nazwę sali konferencyjnej.'})
        except ObjectDoesNotExist:
            pass
        
        capacity = request.POST.get('capacity')
        if int(capacity) < 1:
            return render(request, 'add_room.html', {'error': 'Pojemność sali konferencyjnej nie może być ujemna.'})
        
        if request.POST.get('projector') == None:
            projector = False
        else:
            projector = True

        models.Rooms.objects.create(name=name, capacity=capacity, projector=projector)

        return redirect('/')

class ShowRooms(View):
    def get(self, request) -> HttpResponse:
        try:
            rooms = models.Rooms.objects.all()
        except ObjectDoesNotExist:
            return HttpResponse('Brak dostępnych sal!')
        reservations = models.Reservations.objects.all()
        reservations = reservations.filter(date__exact=date.today())

        for room in rooms:
            if reservations.filter(room=room):
                room.reserved = True

        return render(request, 'rooms.html', {'rooms': rooms,})

class ShowRoom(View):
    def get(self, request, id: int) -> HttpResponse:
        room = models.Rooms.objects.get(pk=id)

        reservations = models.Reservations.objects.all()
        reservations = reservations.filter(room=room)
        reservations = reservations.filter(date__gte=date.today()).order_by('date')
        return render(request, 'room.html', {'room': room,
                                             'reservations': reservations})

class ModifyRoom(View):
    def get(self, request, id: int) -> HttpResponse:
        room = models.Rooms.objects.get(pk=id)

        return render (request, 'room_modify.html', {'room': room})

    def post(self, request, id: int) -> HttpResponse:
        room = models.Rooms.objects.get(pk=id)

        name = request.POST.get('name')
        if name == '':
            return render(request, 'room_modify.html', {'error': 'Musisz podać nazwę sali konferencyjnej.',
                                                        'room': room})
        try:
            rooms = models.Rooms.objects.get(name__iexact=name)
            return render(request, 'room_modify.html', {'error': 'Musisz podać unikatową nazwę sali konferencyjnej.',
                                                        'room': room})
        except ObjectDoesNotExist:
            pass
        room.name = name

        capacity = request.POST.get('capacity')
        if int(capacity) < 1:
            return render(request, 'room_modify.html', {'error': 'Pojemność sali konferencyjnej nie może być ujemna.',
                                                        'room': room})
        room.capacity = capacity
        
        if request.POST.get('projector') == None:
            projector = False
        else:
            projector = True
        room.projector = projector

        room.save()
        
        return redirect('/')

class DeleteRoom(View):
    def get(self, request, id: int) -> HttpResponse:
        room = models.Rooms.objects.get(pk=id)
        room.delete()

        return redirect('/')

class ReserveRoom(View):
    def get(self, request, id: int) -> HttpResponse:
        return render(request, 'room_reserve.html')

    def post(self, request, id: int) -> HttpResponse:
        room = models.Rooms.objects.get(pk=id)
        reservations = models.Reservations.objects.all()
        date_ = request.POST.get('date')
        date_ = date(int(date_[:4]), int(date_[5:7]), int(date_[8:10]))
        reservations = reservations.filter(room=room)
        reservations = reservations.filter(date__exact=date_)
        if not reservations:
            if date.today() > date_:
                return HttpResponse('przeszłość')  # TODO: error
            # else:
            models.Reservations.objects.create(date=date_, room=room, comment=request.POST.get('comment'))
            return redirect('/')
        # models.Reservations.objects.create(date='2021-05-05', room=room, comment='komentarz')
        return HttpResponse(reservations)
