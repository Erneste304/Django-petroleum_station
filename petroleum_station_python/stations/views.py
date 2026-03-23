from django.shortcuts import render, get_object_or_404, redirect
from .models import Station
from .forms import StationForm
from users.decorators import role_required

@role_required('admin', 'accountant', 'staff', 'partner')
def station_list(request):
    stations = Station.objects.all()
    return render(request, 'stations/station_list.html', {'stations': stations})

@role_required('admin')
def station_create(request):
    if request.method == 'POST':
        form = StationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('stations:station_list')
    else:
        form = StationForm()
    return render(request, 'stations/station_form.html', {'form': form, 'title': 'Add Station'})

@role_required('admin')
def station_update(request, pk):
    station = get_object_or_404(Station, pk=pk)
    if request.method == 'POST':
        form = StationForm(request.POST, instance=station)
        if form.is_valid():
            form.save()
            return redirect('stations:station_list')
    else:
        form = StationForm(instance=station)
    return render(request, 'stations/station_form.html', {'form': form, 'title': 'Edit Station'})

@role_required('admin')
def station_delete(request, pk):
    station = get_object_or_404(Station, pk=pk)
    if request.method == 'POST':
        station.delete()
        return redirect('stations:station_list')
    return render(request, 'stations/station_confirm_delete.html', {'station': station})
