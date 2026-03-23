from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from stations.models import Station
from sales.models import Sale
from inventory.models import FuelType, Tank
from loyalty.models import LoyaltyRedemption
from services.models import CarWashService
from .models import User, StaffReport, Customer, InternalMessage, AuditLog, GlobalShareConfig, PartnerShare, ShareTransaction
from .forms import (
    UserCreateForm, UserEditForm, ProfileUpdateForm, InternalMessageForm, 
    ShareTransactionForm, GlobalShareConfigForm, PartnerShareForm
)
from .report_forms import StaffReportForm, ApprovalNoteForm, RejectionForm
from .decorators import role_required
from django.utils import timezone
from django.contrib import messages
from decimal import Decimal


def login_view(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('users:dashboard')
        else:
            error = 'Invalid username or password. Please try again.'
    return render(request, 'users/login.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('users:login')



@login_required
def dashboard(request):
    stations_count = Station.objects.count()
    total_sales = Sale.objects.count()
    latest_sales = Sale.objects.order_by('-sale_date')[:5]
    fuel_types = FuelType.objects.all()
    tanks = Tank.objects.all()
    
    # Calculate percentages for tanks
    for tank in tanks:
        if tank.capacity > 0:
            tank.percentage = (tank.current_stock / tank.capacity) * 100
        else:
            tank.percentage = 0
    
    context = {
        'stations_count': stations_count,
        'total_sales': total_sales,
        'latest_sales': latest_sales,
        'fuel_types': fuel_types,
        'tanks': tanks,
    }

    if request.user.role == 'customer' and request.user.customer:
        customer = request.user.customer
        context['customer_sales'] = Sale.objects.filter(customer=customer).order_by('-sale_date')[:5]
        context['customer_redemptions'] = LoyaltyRedemption.objects.filter(customer=customer).order_by('-redeemed_date')[:5]
        context['available_services'] = CarWashService.objects.all()
        # Calculate some stats for the top row
        context['my_total_purchases'] = Sale.objects.filter(customer=customer).count()
        context['my_total_spent'] = sum(s.total_amount for s in Sale.objects.filter(customer=customer))
        # Points can be calculated or retrieved. For this example we'll show count of rewards available.
        from loyalty.models import LoyaltyReward
        context['rewards_count'] = LoyaltyReward.objects.count()

    if request.user.role == 'partner':
        share_config = GlobalShareConfig.objects.first()
        if not share_config:
            share_config = GlobalShareConfig.objects.create(current_price=1500.00)
        
        partner_share, created = PartnerShare.objects.get_or_create(partner=request.user)
        
        context['share_config'] = share_config
        context['partner_share'] = partner_share
        context['share_transactions'] = ShareTransaction.objects.filter(partner=request.user).order_by('-timestamp')[:5]

    return render(request, 'users/dashboard.html', context)

@login_required
@role_required('admin')
def user_list(request):
    users = User.objects.all()
    return render(request, 'users/user_list.html', {'users': users})

@login_required
@role_required('admin')
def user_create(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:user_list')
    else:
        form = UserCreateForm()
    return render(request, 'users/user_form.html', {'form': form, 'title': 'Create User'})

@login_required
@role_required('admin')
def user_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('users:user_list')
    else:
        form = UserEditForm(instance=user)
    return render(request, 'users/user_form.html', {'form': form, 'title': f'Edit User: {user.username}'})

@login_required
@role_required('admin')
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if user == request.user:
        messages.error(request, "You cannot delete your own account.")
    else:
        username = user.username
        user.delete()
        messages.success(request, f"User {username} deleted successfully.")
    return redirect('users:user_list')

@login_required
@role_required('admin')
def user_toggle_status(request, pk):
    user = get_object_or_404(User, pk=pk)
    if user == request.user:
        messages.error(request, "You cannot deactivate your own account.")
    else:
        user.is_active = not user.is_active
        user.save()
        status = "activated" if user.is_active else "deactivated"
        messages.success(request, f"User {user.username} {status} successfully.")
    return redirect('users:user_list')

@login_required
def report_list(request):
    """
    List reports. 
    Admin sees all. 
    Accountant sees financial.
    Staff sees own.
    """
    if request.user.is_admin:
        reports = StaffReport.objects.all()
    elif request.user.is_accountant:
        reports = StaffReport.objects.all()
    else:
        reports = StaffReport.objects.filter(submitted_by=request.user)
        
    return render(request, 'users/report_list.html', {'reports': reports})

@login_required
@role_required('staff', 'accountant')
def report_create(request):
    """Staff only creates reports"""
    if request.method == 'POST':
        form = StaffReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.submitted_by = request.user
            report.save()
            messages.success(request, 'Report submitted successfully.')
            return redirect('users:report_list')
    else:
        form = StaffReportForm()
    return render(request, 'users/report_form.html', {'form': form})

@login_required
@role_required('accountant', 'admin')
def report_accountant_approve(request, pk):
    report = get_object_or_404(StaffReport, pk=pk)
    if report.status != 'pending':
        messages.error(request, 'Report is not pending.')
        return redirect('users:report_list')
        
    if request.method == 'POST':
        form = ApprovalNoteForm(request.POST)
        if form.is_valid():
            report.accountant_approved = True
            report.accountant_approved_by = request.user
            report.accountant_approved_at = timezone.now()
            report.accountant_note = form.cleaned_data.get('note', '')
            report.status = 'accountant_approved'
            report.save()
            messages.success(request, 'Report operationally approved.')
            return redirect('users:report_list')
    else:
        form = ApprovalNoteForm()
        
    return render(request, 'users/report_approve.html', {
        'form': form, 
        'report': report,
        'title': 'Operational Approval (Accountant)',
        'action_url': 'users:report_accountant_approve'
    })

@login_required
@role_required('admin')
def report_admin_approve(request, pk):
    report = get_object_or_404(StaffReport, pk=pk)
    if report.status != 'accountant_approved':
        messages.error(request, 'Report must be approved by accountant first.')
        return redirect('users:report_list')
        
    if request.method == 'POST':
        form = ApprovalNoteForm(request.POST)
        if form.is_valid():
            report.admin_approved = True
            report.admin_approved_by = request.user
            report.admin_approved_at = timezone.now()
            report.admin_note = form.cleaned_data.get('note', '')
            report.status = 'admin_approved'
            report.save()
            messages.success(request, 'Report finalized and financially approved.')
            return redirect('users:report_list')
    else:
        form = ApprovalNoteForm()
        
    return render(request, 'users/report_approve.html', {
        'form': form, 
        'report': report,
        'title': 'Final Financial Approval (Admin)',
        'action_url': 'users:report_admin_approve'
    })

@login_required
@role_required('admin', 'accountant')
def report_reject(request, pk):
    report = get_object_or_404(StaffReport, pk=pk)
    if report.status in ['admin_approved', 'rejected']:
        messages.error(request, 'Cannot reject this report.')
        return redirect('users:report_list')
        
    if request.method == 'POST':
        form = RejectionForm(request.POST)
        if form.is_valid():
            report.status = 'rejected'
            report.rejection_reason = form.cleaned_data.get('reason', '')
            report.save()
            messages.success(request, 'Report rejected.')
            return redirect('users:report_list')
    else:
        form = RejectionForm()
        
    return render(request, 'users/report_reject.html', {'form': form, 'report': report})

@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('users:profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    
    return render(request, 'users/profile.html', {'user': request.user, 'form': form})

@login_required
@role_required('receptionist')
def report_issue(request, sale_id):
    sale = get_object_or_404(Sale, pk=sale_id)
    if request.method == 'POST':
        form = InternalMessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.related_sale_id = sale_id
            msg.save()
            messages.success(request, 'Issue reported successfully.')
            return redirect('sales:sale_list')
    else:
        form = InternalMessageForm(initial={'subject': f'Issue with Sale #{sale_id}'})
    return render(request, 'users/report_issue.html', {'form': form, 'sale': sale})

@login_required
@role_required('admin', 'accountant', 'staff')
def inbox(request):
    messages = InternalMessage.objects.filter(recipient_role=request.user.role, is_resolved=False).order_by('-timestamp')
    return render(request, 'users/inbox.html', {'messages': messages})

@login_required
@role_required('admin')
def audit_logs(request):
    logs = AuditLog.objects.all().order_by('-timestamp')
    return render(request, 'users/audit_logs.html', {'logs': logs})

@login_required
@role_required('partner')
def share_transaction(request):
    config = GlobalShareConfig.objects.first()
    if request.method == 'POST':
        form = ShareTransactionForm(request.POST)
        if form.is_valid():
            trans_type = form.cleaned_data['transaction_type']
            amount = form.cleaned_data['amount_shares']
            price = config.current_price
            total = amount * price
            commission = Decimal('0.00')

            partner_share, created = PartnerShare.objects.get_or_create(partner=request.user)

            if trans_type == 'sell':
                if partner_share.total_shares < amount:
                    messages.error(request, 'Insufficient shares to sell.')
                    return redirect('users:dashboard')
                commission = total * config.commission_percentage

            ShareTransaction.objects.create(
                partner=request.user,
                transaction_type=trans_type,
                amount_shares=amount,
                price_per_share=price,
                total_amount=total,
                commission_deducted=commission,
                recorded_by=request.user,
                status='pending'
            )
            messages.success(request, f'Transaction request for {amount} shares submitted and awaiting review.')
            return redirect('users:dashboard')
    
    return redirect('users:dashboard')

@login_required
@role_required('admin', 'accountant', 'staff')
def share_request_list(request):
    """Admin/Accountant/Staff can see all share operations."""
    transactions = ShareTransaction.objects.all().order_by('-timestamp')
    return render(request, 'users/share_request_list.html', {'transactions': transactions})

@login_required
@role_required('accountant', 'admin')
def share_accountant_approve(request, pk):
    trans = get_object_or_404(ShareTransaction, pk=pk)
    if trans.status != 'pending':
        messages.error(request, 'Transaction is not pending evaluation.')
        return redirect('users:share_request_list')
    
    trans.status = 'accountant_approved'
    trans.accountant_approved_by = request.user
    trans.accountant_approved_at = timezone.now()
    trans.save()
    messages.success(request, f'Transaction for {trans.partner.username} operationally approved.')
    return redirect('users:share_request_list')

@login_required
@role_required('admin')
def share_admin_approve(request, pk):
    trans = get_object_or_404(ShareTransaction, pk=pk)
    if trans.status != 'accountant_approved':
        messages.error(request, 'Transaction must be checked by accountant first.')
        return redirect('users:share_request_list')
    
    # EXECUTE: Update the actual balances
    partner_share, created = PartnerShare.objects.get_or_create(partner=trans.partner)
    
    if trans.transaction_type == 'buy':
        partner_share.total_shares += trans.amount_shares
        partner_share.total_investment += trans.total_amount
    elif trans.transaction_type == 'sell':
        if partner_share.total_shares < trans.amount_shares:
            messages.error(request, 'Partner has insufficient shares for this liquidation.')
            trans.status = 'rejected'
            trans.rejection_reason = "Insufficient shares at time of final execution."
            trans.save()
            return redirect('users:share_request_list')
        partner_share.total_shares -= trans.amount_shares
        # Note: investment value could be adjusted here based on book value if needed

    partner_share.save()
    
    trans.status = 'approved'
    trans.admin_approved_by = request.user
    trans.admin_approved_at = timezone.now()
    trans.save()
    
    messages.success(request, f'Transaction finalized. {trans.partner.username}\'s portfolio updated.')
    return redirect('users:share_request_list')

@login_required
@role_required('admin', 'accountant')
def share_reject(request, pk):
    trans = get_object_or_404(ShareTransaction, pk=pk)
    if trans.status in ['approved', 'rejected']:
        messages.error(request, 'This transaction status cannot be changed.')
        return redirect('users:share_request_list')
        
    if request.method == 'POST':
        reason = request.POST.get('reason', 'No reason provided.')
        trans.status = 'rejected'
        trans.rejection_reason = reason
        trans.save()
        messages.success(request, 'Transaction request rejected.')
        return redirect('users:share_request_list')
    
    return render(request, 'users/share_reject.html', {'transaction': trans})

@login_required
@role_required('admin', 'staff')
def share_config_update(request):
    config = GlobalShareConfig.objects.first()
    if not config:
        config = GlobalShareConfig.objects.create()
        
    if request.method == 'POST':
        form = GlobalShareConfigForm(request.POST, instance=config)
        if form.is_valid():
            form.save()
            messages.success(request, 'Global share price and commission settings updated.')
            return redirect('users:dashboard')
    else:
        form = GlobalShareConfigForm(instance=config)
    return render(request, 'users/share_config_form.html', {'form': form})

@login_required
@role_required('admin', 'staff')
def partner_share_list(request):
    shares = PartnerShare.objects.all()
    return render(request, 'users/partner_share_list.html', {'shares': shares})

@login_required
@role_required('admin', 'staff')
def partner_share_edit(request, pk):
    share = get_object_or_404(PartnerShare, pk=pk)
    if request.method == 'POST':
        form = PartnerShareForm(request.POST, instance=share)
        if form.is_valid():
            form.save()
            messages.success(request, f'Portfolio for {share.partner.username} manually adjusted.')
            return redirect('users:partner_share_list')
    else:
        form = PartnerShareForm(instance=share)
    return render(request, 'users/partner_share_edit.html', {'form': form, 'share': share})

@login_required
@role_required('admin', 'staff')
def partner_share_delete(request, pk):
    share = get_object_or_404(PartnerShare, pk=pk)
    username = share.partner.username
    share.delete()
    messages.success(request, f'Share profile for {username} deleted.')
    return redirect('users:partner_share_list')

@login_required
def partner_message(request):
    if request.method == 'POST':
        form = InternalMessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.save()
            messages.success(request, 'Idea/Comment shared successfully with the team.')
        else:
            messages.error(request, 'Failed to send message. Please check the form.')
    return redirect('users:dashboard')
