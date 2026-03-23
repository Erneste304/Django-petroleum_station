from django.shortcuts import render, get_object_or_404, redirect
from .models import FuelType, Tank, Pump, FuelDelivery
from .forms import FuelDeliveryForm, FuelPriceForm, TankForm
from users.decorators import role_required
from django.utils import timezone
from django.contrib import messages
from users.models import AuditLog

@role_required('admin', 'accountant', 'staff', 'partner')
def fuel_status(request):
    fuel_types = FuelType.objects.all()
    tanks = Tank.objects.all()
    pumps = Pump.objects.all()
    return render(request, 'inventory/fuel_status.html', {
        'fuel_types': fuel_types,
        'tanks': tanks,
        'pumps': pumps
    })

@role_required('admin', 'staff')
def record_delivery(request):
    """Record a new fuel delivery, update tank stock."""
    if request.method == 'POST':
        form = FuelDeliveryForm(request.POST)
        if form.is_valid():
            delivery = form.save(commit=False)
            # Update tank stock
            tank = delivery.tank
            old_stock = tank.current_stock
            tank.current_stock += delivery.quantity
            if tank.current_stock > tank.capacity:
                tank.current_stock = tank.capacity
            tank.save(update_fields=['current_stock'])
            delivery.save()
            
            # Audit the stock update
            AuditLog.objects.create(
                model_name='Tank',
                object_id=str(tank.pk),
                changed_by=request.user,
                old_data={'current_stock': str(old_stock)},
                new_data={'current_stock': str(tank.current_stock)},
                timestamp=timezone.now()
            )
            
            messages.success(request, f"Recorded {delivery.quantity}L delivery to {tank}.")
            return redirect('inventory:fuel_status')
    else:
        form = FuelDeliveryForm()
    return render(request, 'inventory/delivery_form.html', {'form': form, 'title': 'Record Fuel Delivery'})

@role_required('admin', 'accountant')
def update_price(request, pk):
    """Update price per liter for a fuel type."""
    fuel = get_object_or_404(FuelType, pk=pk)
    if request.method == 'POST':
        form = FuelPriceForm(request.POST, instance=fuel)
        if form.is_valid():
            form.save()
            messages.success(request, f"Price for {fuel.fuel_name} updated.")
            return redirect('inventory:fuel_status')
    else:
        form = FuelPriceForm(instance=fuel)
    return render(request, 'inventory/update_price_form.html', {'form': form, 'fuel': fuel})

@role_required('admin')
def tank_create(request):
    if request.method == 'POST':
        form = TankForm(request.POST)
        if form.is_valid():
            tank = form.save()
            AuditLog.objects.create(
                model_name='Tank',
                object_id=str(tank.pk),
                changed_by=request.user,
                new_data={'fuel': tank.fuel.fuel_name, 'capacity': str(tank.capacity), 'current_stock': str(tank.current_stock)}
            )
            messages.success(request, "Tank created successfully.")
            return redirect('inventory:fuel_status')
    else:
        form = TankForm()
    return render(request, 'inventory/tank_form.html', {'form': form, 'title': 'Add New Tank'})

@role_required('admin')
def tank_update(request, pk):
    tank = get_object_or_404(Tank, pk=pk)
    if request.method == 'POST':
        old_data = {'capacity': str(tank.capacity), 'current_stock': str(tank.current_stock)}
        form = TankForm(request.POST, instance=tank)
        if form.is_valid():
            tank = form.save()
            new_data = {'capacity': str(tank.capacity), 'current_stock': str(tank.current_stock)}
            AuditLog.objects.create(
                model_name='Tank',
                object_id=str(tank.pk),
                changed_by=request.user,
                old_data=old_data,
                new_data=new_data
            )
            messages.success(request, "Tank updated successfully.")
            return redirect('inventory:fuel_status')
    else:
        form = TankForm(instance=tank)
    return render(request, 'inventory/tank_form.html', {'form': form, 'title': 'Edit Tank'})

@role_required('admin')
def tank_delete(request, pk):
    tank = get_object_or_404(Tank, pk=pk)
    tank_id = tank.tank_id
    tank.delete()
    AuditLog.objects.create(
        model_name='Tank',
        object_id=str(tank_id),
        changed_by=request.user,
        old_data={'status': 'deleted'}
    )
    messages.success(request, "Tank deleted successfully.")
    return redirect('inventory:fuel_status')
