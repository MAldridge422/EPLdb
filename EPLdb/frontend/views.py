from django.shortcuts import render

def index(request):
    return render(request, 'index.html',)

def teams(request):
    return render(request, 'teams.html',)

def positions(request):
    return render(request, 'positions.html',)

def bookings(request):
    return render(request, 'bookings.html',)

def goals(request):
    return render(request, 'goals.html',)

def raw_data(request):
    return render(request, 'raw_data.html',)
