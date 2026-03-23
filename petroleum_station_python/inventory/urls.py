from django.urls import path
from django.views.generic import RedirectView
from . import views

app_name = 'inventory'


urlpatterns = [
    path('', RedirectView.as_view(url='/inventory/status/', permanent=False)),
    path('status/', views.fuel_status, name='fuel_status'),
    path('delivery/record/', views.record_delivery, name='record_delivery'),
    path('price/update/<int:pk>/', views.update_price, name='update_price'),
    path('tank/create/', views.tank_create, name='tank_create'),
    path('tank/edit/<int:pk>/', views.tank_update, name='tank_update'),
    path('tank/delete/<int:pk>/', views.tank_delete, name='tank_delete'),
]

