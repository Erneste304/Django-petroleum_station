from django.db import models
from users.models import Customer

class CarWashService(models.Model):
    service_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    estimated_duration_minutes = models.IntegerField(default=30)

    class Meta:
        db_table = 'car_wash_service'
        managed = False

    def __str__(self):
        return self.name

class CarWashBooking(models.Model):
    booking_id = models.AutoField(primary_key=True)
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    service = models.ForeignKey(CarWashService, on_delete=models.CASCADE)
    booking_date = models.DateField()
    booking_time = models.TimeField()
    vehicle_plate = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'car_wash_booking'
        managed = False

    def __str__(self):
        return f"Booking {self.booking_id} - {self.customer.name} - {self.vehicle_plate}"

