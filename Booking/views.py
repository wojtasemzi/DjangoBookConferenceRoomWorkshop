from django.http.response import HttpResponse
from django.shortcuts import redirect, render

from django.views import View
from django.core.exceptions import ObjectDoesNotExist

from Booking import models

class AddRoom(View):
    def get(self, request):
        return render(request, 'add_room.html')

    def post(self, request):
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
    def get(self, request):
        try:
            rooms = models.Rooms.objects.all()
        except ObjectDoesNotExist:
            return HttpResponse('Brak dostępnych sal!')

        return render(request, 'rooms.html', {'rooms': rooms})
