from django.db import models
from stations.models import Station

class FuelType(models.Model):
    fuel_id = models.AutoField(primary_key=True)
    fuel_name = models.CharField(max_length=50, unique=True)
    price_per_liter = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'fuel_type'
        managed = False

    def __str__(self):
        return self.fuel_name

class Tank(models.Model):
    tank_id = models.AutoField(primary_key=True)
    fuel = models.ForeignKey(FuelType, on_delete=models.CASCADE)
    capacity = models.DecimalField(max_digits=10, decimal_places=2)
    current_stock = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'tank'
        managed = False

    def __str__(self):
        return f"Tank for {self.fuel.fuel_name}"

class Pump(models.Model):
    pump_id = models.AutoField(primary_key=True)
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    fuel = models.ForeignKey(FuelType, on_delete=models.CASCADE)

    class Meta:
        db_table = 'pump'
        managed = False

    def __str__(self):
        return f"Pump at {self.station.station_name} - {self.fuel.fuel_name}"

class Supplier(models.Model):
    name = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.name

class FuelDelivery(models.Model):
    delivery_id = models.AutoField(primary_key=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    tank = models.ForeignKey(Tank, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'fuel_delivery'
        managed = False

    def __str__(self):
        return f"Delivery of {self.quantity} to {self.tank}"

