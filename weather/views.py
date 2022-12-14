from django.shortcuts import render, redirect
from math import ceil
import requests
from .models import City
from .forms import CityForm
import os


def mainPage(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid='
    url += f"{os.environ.get('WEATHER_API_KEY')}"

    cities = City.objects.all()

    form = CityForm()

    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            try:
                city = City.objects.get(name=form.cleaned_data.get('name'))
                city.delete()
            except:
                print("No such city in the database!")
            city_weather = requests.get(url.format(form.cleaned_data.get('name'))).json()
            print(city_weather)
            if 'message' not in city_weather:
                form.save()
                if len(cities) > 10:
                    cities[0].delete()
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

    weather_data.reverse()

    context = {'weather_data': weather_data, 'form': form}
    return render(request, 'main.html', context)


def deleteWeather(request, name):
    city = City.objects.get(name=name)
    if request.method == 'POST':
        city.delete()
        return redirect('home')
    context = {'city': city}
    return render(request, 'delete_form.html', context)


def fullForecast(request, name):
    city = City.objects.get(name=name)
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city.name}&appid={os.environ.get('WEATHER_API_KEY')}&units=metric"
    forecast = requests.get(url).json()
    day, time = forecast['list'][0]['dt_txt'].split()
    today = []
    for d in forecast['list']:
        if day in d['dt_txt']:
            today.append(d)
        else:
            break
    print(today)
    parts = forecast['list']
    context = {'parts': today, 'city': forecast['city']['name'], 'country': forecast['city']['country'], 'day': day}
    return render(request, 'full_forecast.html', context)
