from django.urls import path
from . import views

app_name = 'services'


urlpatterns = [
    path('bookings/', views.booking_list, name='booking_list'),
    path('bookings/create/', views.booking_create, name='booking_create'),
]

