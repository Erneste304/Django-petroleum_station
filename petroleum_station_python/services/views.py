from django.shortcuts import render, redirect, get_object_or_404
from .models import CarWashBooking, CarWashService
from .forms import CarWashBookingForm
from users.decorators import role_required

@role_required('admin', 'accountant', 'staff', 'receptionist')
def booking_list(request):
    bookings = CarWashBooking.objects.all().order_by('-booking_date')
    services = CarWashService.objects.all()
    context = {
        'bookings': bookings,
        'services': services
    }
    return render(request, 'services/booking_list.html', context)

@role_required('admin', 'staff', 'receptionist')
def booking_create(request):
    if request.method == 'POST':
        form = CarWashBookingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('services:booking_list')
    else:
        form = CarWashBookingForm()
    return render(request, 'services/booking_form.html', {'form': form})
