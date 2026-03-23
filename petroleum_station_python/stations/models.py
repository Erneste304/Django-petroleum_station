from django.db import models

class Station(models.Model):
    station_id = models.AutoField(primary_key=True)
    station_name = models.CharField(max_length=100)
    location = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'station'
        managed = False

    def __str__(self):
        return self.station_name

class Employee(models.Model):
    employee_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    position = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True, null=True)
    station = models.ForeignKey(Station, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'employee'
        managed = False

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

