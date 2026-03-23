from django.urls import path
from . import views

app_name = 'loyalty'


urlpatterns = [
    path('rewards/', views.reward_list, name='reward_list'),
    path('rewards/create/', views.reward_create, name='reward_create'),
]

