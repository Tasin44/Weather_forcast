from django.shortcuts import render
import requests   #pip install requests
# A Python library to make HTTP requests to external services (in this case, the OpenWeatherMap API).
import pycountry  # pip install pycountry


# Function to get the full country name
def get_country_name(country_code):
    try:
        country = pycountry.countries.get(alpha_2=country_code)
        return country.name
    except KeyError:
        return country_code  # Return the code if the country isn't found


#This function sends a request to the OpenWeatherMap API to get weather data for the specified city.
def get_weather(city):
    base_url = "https://api.openweathermap.org/data/2.5/weather" #it's API URL for fetching current weather data.
    api_key = "fbda0395bab6dc016deced0f29c5411c" #It's used to authenticate the request.
    parameters = {
        'q': city,
        'appid': api_key,
        'units': 'metric' #for temperature in Celsius.
    }
    response = requests.get(base_url, params=parameters) #This  method sends a GET request to the API with these parameters.
    if response.status_code == 200: #Explained later
        return response.json()
    else:
        return None


def home(request):
    city = request.GET.get('city', '') #This retrieves the value of the city from the GET request, or assigns an empty string if no city is entered.
    icon_url = 'https://openweathermap.org/img/wn/10d@2x.png' #default weather icon in case the API doesn't return any valid data.
    weather = weather_description = city_name = country = wind_speed = pressure = humidity = temperature = country_code = latitude =longitude= None
    #All variables are initialized to None to avoid errors if no data is fetched.
    
    if city:
        weather_data_result = get_weather(city)

        if weather_data_result:
            icon_id = weather_data_result['weather'][0]['icon']
            icon_url = f"https://openweathermap.org/img/wn/{icon_id}@2x.png" 
#icon_url:URL for the specific city's weather condition icon,it's necessary to update the icon based on city's current weather
            weather = weather_data_result['weather'][0]['main']
            weather_description = weather_data_result['weather'][0]['description']
            city_name = weather_data_result['name']
            country_code = weather_data_result['sys']['country']
            # coord = weather_data_result['coord']
            latitude = weather_data_result['coord']['lat']
            longitude = weather_data_result['coord']['lon']
            wind_speed = weather_data_result['wind']['speed']
            pressure = weather_data_result['main']['pressure']
            humidity = weather_data_result['main']['humidity']
            temperature = weather_data_result['main']['temp']
            
            # Get full country name
            country = get_country_name(country_code)

    return render(request, 'index.html', {
        'icon_url': icon_url,
        'weather': weather,
        'weather_description': weather_description,
        'city': city_name,
        'country_code': country_code,
        'country': country,
        'latitude': latitude,
        'longitude': longitude,
        'wind_speed': wind_speed,
        'pressure': pressure,
        'humidity': humidity,
        'temperature': temperature,
    })


'''
why the response's status code == 200 means successful? 
why not any other number instead of 200? 
and can you explain " the function returns the weather data in JSON format.

Why is 200 used to indicate a successful HTTP response?
In the HTTP (Hypertext Transfer Protocol) standard, different status codes indicate the result of an HTTP request. These codes are grouped into categories based on their purpose, each represented by a 3-digit number:

    1xx (Informational) – The request was received, and the process is continuing.
    2xx (Success) – The request was successfully received, understood, and accepted.
    3xx (Redirection) – Further action needs to be taken to complete the request.
    4xx (Client Error) – The request contains bad syntax or cannot be fulfilled.
    5xx (Server Error) – The server failed to fulfill a valid request.

The status code 200 specifically means "OK" in the HTTP standard. This means that the request was successful, the server understood the request, processed it, and is returning the expected content. Other status codes in the 2xx range also indicate successful requests but with different meanings:

    201 Created: The request was successful, and a new resource was created.
    202 Accepted: The request was accepted for processing, but the processing hasn't completed.

The reason 200 is used is simply part of the agreed-upon convention in the HTTP protocol. It’s a universally understood signal that the response from the server is valid and contains the expected data.
Explanation of "returns the weather data in JSON format"

The line response.json() converts the server's response (which is likely in JSON format) into a Python dictionary or list, depending on the structure of the JSON data. JSON (JavaScript Object Notation) is a lightweight data format that is easy for humans to read and write and easy for machines to parse and generate.

In this case, the weather data returned by the OpenWeather API is in JSON format, meaning the data is structured in key-value pairs. Here’s an example of what the weather data might look like in JSON:

json

{
    "weather": [
        {
            "main": "Clear",
            "description": "clear sky",
            "icon": "01d"
        }
    ],
    "main": {
        "temp": 25.76,
        "pressure": 1013,
        "humidity": 53
    },
    "wind": {
        "speed": 3.09
    },
    "sys": {
        "country": "US"
    },
    "name": "New York"
}

The response.json() call transforms this JSON structure into a Python dictionary, which can then be accessed in the code. For example, to get the temperature, you could access weather_data['main']['temp'].




explanation of if weather_data_result:

3. weather = weather_data_result['weather'][0]['main']
This extracts the main weather condition (e.g., "Clear," "Rain," "Clouds") from the JSON data under 'weather'. The first (and usually only) weather description is selected from the list.
    
4. weather_description = weather_data_result['weather'][0]['description']
This line retrieves the more detailed description of the weather, such as "clear sky," "light rain," or "broken clouds." It's a human-readable description of the weather condition.

5. city_name = weather_data_result['name']
The city name is extracted here. This is the city the user searched for, and it appears under the key 'name' in the JSON.

6. country = weather_data_result['sys']['country']
This line pulls the country code from the 'sys' section of the weather data. The country is represented by a two-letter ISO country code (like "US" for the United States).

7. country_code = weather_data_result['sys']['country']
This is similar to the previous line, pulling the country code from the same place. 

wind_speed = weather_data_result['wind']['speed']
This extracts the wind speed from the weather data under the 'wind' key.
    
10. pressure = weather_data_result['main']['pressure']
This line retrieves the atmospheric pressure in hPa (hectopascals) from the 'main' section of the weather data.

11. humidity = weather_data_result['main']['humidity']
Here, the humidity percentage is extracted from the 'main' section.

12. temperature = weather_data_result['main']['temp']
This extracts the temperature in degrees Celsius (as requested with the units: 'metric' parameter when making the API call) from the 'main' section of the weather data.


'''