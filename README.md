# Weather Forecast Application

![Screenshot 2025-06-15 at 21-48-27 Weather Forecast App](https://github.com/user-attachments/assets/a95af261-6449-4801-bde8-9c865b4a7959)

A responsive web application built with Django that provides current weather conditions and 5-day forecasts for any city worldwide using the OpenWeatherMap API.

## Features

- 🌦️ **Current Weather Data**
  - Temperature (current, feels-like, min/max)
  - Humidity, pressure, wind speed/direction
  - Visibility and cloudiness
  - Sunrise and sunset times

- 📅 **5-Day Forecast**
  - Daily high/low temperatures
  - Weather conditions with icons
  - Humidity levels

- 🌍 **Location Details**
  - City name and country
  - Geographic coordinates
  - Local time

- 🎨 **Modern UI**
  - Responsive design (works on mobile, tablet, and desktop)
  - Clean, intuitive interface
  - Animated weather icons

## Technologies Used

- **Backend**: Django (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **API**: OpenWeatherMap
- **Libraries**: 
  - `requests` for API calls
  - `pycountry` for country code conversion
  - `datetime` for time handling

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/weather-forecast-app.git
   cd weather-forecast-app
2. **Set up a virtual environment (recommended)**
```
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
3. ***Install dependencies***

```
pip install django requests pycountry
```
4. ***Set up environment variables***

Create a .env file in your project directory:
OPENWEATHER_API_KEY=your_api_key_here


5. ***Run the development server***
```
python manage.py runserver
```
6. Access the application

Open your browser and visit:

```
http://127.0.0.1:8000
```
