from django.shortcuts import render, redirect, get_object_or_404
from .models import Sale
from .forms import SaleForm
from users.decorators import role_required
from users.models import AuditLog
from django.contrib import messages
import json

@role_required('admin', 'accountant', 'staff', 'receptionist')
def sale_list(request):
    sales = Sale.objects.all().order_by('-sale_date')
    return render(request, 'sales/sale_list.html', {'sales': sales})

@role_required('admin', 'accountant', 'staff', 'receptionist')
def sale_create(request):
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sales:sale_list')
    else:
        form = SaleForm()
    return render(request, 'sales/sale_form.html', {'form': form, 'title': 'New Sale'})

@role_required('admin', 'accountant', 'staff')
def sale_edit(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    
    def serialize_sale(s):
        return {
            'customer_id': s.customer_id,
            'employee_id': s.employee_id,
            'pump_id': s.pump_id,
            'quantity': str(s.quantity),
            'total_amount': str(s.total_amount),
        }
        
    if request.method == 'POST':
        old_data = serialize_sale(sale)
        form = SaleForm(request.POST, instance=sale)
        if form.is_valid():
            updated_sale = form.save()
            new_data = serialize_sale(updated_sale)
            if old_data != new_data:
                AuditLog.objects.create(
                    model_name='Sale',
                    object_id=str(updated_sale.pk),
                    changed_by=request.user,
                    old_data=old_data,
                    new_data=new_data
                )
            return redirect('sales:sale_list')
    else:
        form = SaleForm(instance=sale)
    return render(request, 'sales/sale_form.html', {'form': form, 'title': 'Edit Sale', 'sale': sale})
@role_required('admin')
def sale_delete(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    sale_id = sale.sale_id
    sale.delete()
    messages.success(request, f"Sale #{sale_id} deleted successfully.")
    return redirect('sales:sale_list')
