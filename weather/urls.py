from django.urls import path
from . import views


urlpatterns = [
    path('', views.mainPage, name='home'),
    path('delete-weather/<str:name>/', views.deleteWeather, name='delete-weather'),
    path('full-forecast/<str:name>/', views.fullForecast, name='full-forecast'),
]