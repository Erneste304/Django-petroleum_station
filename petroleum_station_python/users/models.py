from django.db import models
from django.contrib.auth.models import AbstractUser
from decimal import Decimal

class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True, null=True)
    vehicle_plate = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = 'customer'
        managed = False

    def __str__(self):
        return self.name


class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('staff', 'Staff Member'),
        ('accountant', 'Accountant'),
        ('receptionist', 'Receptionist'),
        ('partner', 'Partner'),
        ('customer', 'Customer'),
    )

    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='customer')
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.username} ({self.role})"

    @property
    def is_admin(self):
        return self.role == 'admin' or self.is_superuser

    @property
    def is_accountant(self):
        return self.role == 'accountant'

    @property
    def is_staff_member(self):
        return self.role == 'staff'


class StaffReport(models.Model):
    REPORT_TYPE_CHOICES = (
        ('operational', 'Operational'),
        ('financial', 'Financial'),
        ('maintenance', 'Maintenance'),
        ('incident', 'Incident Report'),
    )
    STATUS_CHOICES = (
        ('pending', 'Pending Review'),
        ('accountant_approved', 'Accountant Approved'),
        ('admin_approved', 'Admin Approved (Final)'),
        ('rejected', 'Rejected'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    report_type = models.CharField(max_length=30, choices=REPORT_TYPE_CHOICES, default='operational')
    submitted_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='submitted_reports'
    )
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='pending')

    # Stage 1: Accountant approval
    accountant_approved = models.BooleanField(default=False)
    accountant_approved_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='accountant_approvals'
    )
    accountant_approved_at = models.DateTimeField(null=True, blank=True)
    accountant_note = models.TextField(blank=True, null=True)

    # Stage 2: Admin final approval
    admin_approved = models.BooleanField(default=False)
    admin_approved_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='admin_approvals'
    )
    admin_approved_at = models.DateTimeField(null=True, blank=True)
    admin_note = models.TextField(blank=True, null=True)

    # Rejection
    rejection_reason = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        return f"[{self.get_report_type_display()}] {self.title} — {self.get_status_display()}"


class AuditLog(models.Model):
    model_name = models.CharField(max_length=100)
    object_id = models.CharField(max_length=255)
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='audit_logs')
    old_data = models.JSONField(blank=True, null=True)
    new_data = models.JSONField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.model_name} ({self.object_id}) changed by {self.changed_by.username if self.changed_by else 'Unknown'}"


class InternalMessage(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('staff', 'Staff Member'),
        ('accountant', 'Accountant'),
        ('partner', 'Partner'),
        ('receptionist', 'Receptionist'),
    )
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient_role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    subject = models.CharField(max_length=200)
    body = models.TextField()
    related_sale_id = models.IntegerField(blank=True, null=True)  # Optional reference to a problem sale
    is_resolved = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"Message from {self.sender.username} to {self.get_recipient_role_display()} - {self.subject}"


class GlobalShareConfig(models.Model):
    current_price = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('1000.00'))
    commission_percentage = models.DecimalField(max_digits=5, decimal_places=4, default=Decimal('0.0001')) # 0.01%
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Share Config: {self.current_price} RWF"


class PartnerShare(models.Model):
    partner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='share_profile')
    total_shares = models.DecimalField(max_digits=15, decimal_places=4, default=Decimal('0.0000'))
    total_investment = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal('0.00'))

    def __str__(self):
        return f"{self.partner.username}: {self.total_shares} Shares"

    @property
    def current_value(self):
        config = GlobalShareConfig.objects.first()
        price = Decimal('1000.00')
        if config:
            price = config.current_price
        return self.total_shares * price


class ShareTransaction(models.Model):
    TRANSACTION_TYPES = (
        ('buy', 'Buy'),
        ('sell', 'Sell'),
    )
    STATUS_CHOICES = (
        ('pending', 'Pending Review'),
        ('accountant_approved', 'Accountant Approved'),
        ('approved', 'Approved (Final)'),
        ('rejected', 'Rejected'),
    )
    partner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='share_transactions')
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount_shares = models.DecimalField(max_digits=15, decimal_places=4)
    price_per_share = models.DecimalField(max_digits=15, decimal_places=2)
    total_amount = models.DecimalField(max_digits=20, decimal_places=2)
    commission_deducted = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal('0.00'))
    timestamp = models.DateTimeField(auto_now_add=True)
    
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='pending')
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='recorded_share_transactions')
    
    # Accountant approval
    accountant_approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='share_accountant_approvals')
    accountant_approved_at = models.DateTimeField(null=True, blank=True)
    
    # Admin approval
    admin_approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='share_admin_approvals')
    admin_approved_at = models.DateTimeField(null=True, blank=True)
    
    rejection_reason = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.partner.username} - {self.transaction_type} {self.amount_shares} @ {self.price_per_share} ({self.status})"
