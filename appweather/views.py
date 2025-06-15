# views.py
from django.shortcuts import render
from django.http import JsonResponse
import requests
import pycountry
from datetime import datetime
import json

def get_country_name(country_code):
    """Get full country name from country code"""
    try:
        country = pycountry.countries.get(alpha_2=country_code)
        return country.name
    except (KeyError, AttributeError):
        return country_code

def get_weather(city):
    """Fetch weather data from OpenWeatherMap API"""
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    api_key = "fbda0395bab6dc016deced0f29c5411c"  # Consider moving to environment variables
    
    parameters = {
        'q': city,
        'appid': api_key,
        'units': 'metric'
    }
    
    try:
        response = requests.get(base_url, params=parameters, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except requests.exceptions.RequestException:
        return None

def get_forecast(city):
    """Fetch 5-day weather forecast"""
    base_url = "https://api.openweathermap.org/data/2.5/forecast"
    api_key = "fbda0395bab6dc016deced0f29c5411c"
    
    parameters = {
        'q': city,
        'appid': api_key,
        'units': 'metric'
    }
    
    try:
        response = requests.get(base_url, params=parameters, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except requests.exceptions.RequestException:
        return None

def format_forecast_data(forecast_data):
    """Format forecast data for easier template rendering"""
    if not forecast_data:
        return []
    
    daily_forecasts = {}
    
    for item in forecast_data['list'][:15]:  # Get next 5 days (3-hour intervals)
        date = datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d')
        
        if date not in daily_forecasts:
            daily_forecasts[date] = {
                'date': datetime.fromtimestamp(item['dt']).strftime('%A, %B %d'),
                'icon': item['weather'][0]['icon'],
                'description': item['weather'][0]['description'].title(),
                'temp_max': item['main']['temp'],
                'temp_min': item['main']['temp'],
                'humidity': item['main']['humidity'],
                'wind_speed': item['wind']['speed']
            }
        else:
            # Update min/max temperatures
            daily_forecasts[date]['temp_max'] = max(
                daily_forecasts[date]['temp_max'], 
                item['main']['temp']
            )
            daily_forecasts[date]['temp_min'] = min(
                daily_forecasts[date]['temp_min'], 
                item['main']['temp']
            )
    
    return list(daily_forecasts.values())[:5]

def home(request):
    """Main view for weather app"""
    city = request.GET.get('city', '').strip()
    
    context = {
        'searched_city': city,
        'error': None,
        'weather_data': None,
        'forecast_data': [],
    }
    
    if city:
        # Get current weather
        weather_result = get_weather(city)
        
        if weather_result:
            # Get forecast data
            forecast_result = get_forecast(city)
            forecast_data = format_forecast_data(forecast_result)
            
            # Calculate local time
            timezone_offset = weather_result.get('timezone', 0)
            local_time = datetime.utcnow().timestamp() + timezone_offset
            local_time_formatted = datetime.fromtimestamp(local_time).strftime('%I:%M %p')
            
            # Calculate feels like temperature
            feels_like = weather_result['main'].get('feels_like', weather_result['main']['temp'])
            
            # Get additional weather info
            visibility = weather_result.get('visibility', 0) / 1000  # Convert to km
            
            context['weather_data'] = {
                'city_name': weather_result['name'],
                'country': get_country_name(weather_result['sys']['country']),
                'country_code': weather_result['sys']['country'],
                'coordinates': {
                    'lat': weather_result['coord']['lat'],
                    'lon': weather_result['coord']['lon']
                },
                'weather': {
                    'main': weather_result['weather'][0]['main'],
                    'description': weather_result['weather'][0]['description'].title(),
                    'icon': weather_result['weather'][0]['icon'],
                    'icon_url': f"https://openweathermap.org/img/wn/{weather_result['weather'][0]['icon']}@2x.png"
                },
                'temperature': {
                    'current': round(weather_result['main']['temp']),
                    'feels_like': round(feels_like),
                    'min': round(weather_result['main']['temp_min']),
                    'max': round(weather_result['main']['temp_max'])
                },
                'details': {
                    'humidity': weather_result['main']['humidity'],
                    'pressure': weather_result['main']['pressure'],
                    'wind_speed': weather_result['wind']['speed'],
                    'wind_direction': weather_result['wind'].get('deg', 0),
                    'visibility': round(visibility, 1),
                    'cloudiness': weather_result['clouds']['all']
                },
                'sun': {
                    'sunrise': datetime.fromtimestamp(weather_result['sys']['sunrise']).strftime('%I:%M %p'),
                    'sunset': datetime.fromtimestamp(weather_result['sys']['sunset']).strftime('%I:%M %p')
                },
                'local_time': local_time_formatted
            }
            context['forecast_data'] = forecast_data
        else:
            context['error'] = f"Weather data not found for '{city}'. Please check the city name and try again."
    
    return render(request, 'index.html', context)

