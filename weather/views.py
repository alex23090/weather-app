from django.shortcuts import render, redirect
from math import ceil
import requests
from .models import City
from .forms import CityForm
import os


def mainPage(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=c3994ea9cb6a6b70c4001b8c6713dc0a'

    cities = City.objects.all()

    form = CityForm()

    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    weather_data = []

    for city in cities:
        city_weather = requests.get(url.format(city)).json()

        if 'message' not in city_weather:
            weather = {
                'city': city,
                'temperature': ceil((city_weather['main']['temp'] - 32) * 5 / 9),
                'description': city_weather['weather'][0]['description'],
                'icon': city_weather['weather'][0]['icon'],
                'country': city_weather['sys']['country'],
            }
            weather_data.append(weather)
        else:
            city.delete()

    context = {'weather_data': weather_data, 'form': form}
    return render(request, 'main.html', context)


def deleteWeather(request, name):
    city = City.objects.get(name=name)
    if request.method == 'POST':
        city.delete()
        return redirect('home')
    context = {'city': city}
    return render(request, 'delete_form.html', context)
