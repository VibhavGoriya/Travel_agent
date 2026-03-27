# mcp_tools.py
import requests
from datetime import datetime

def get_weather(location: str) -> str:
    """
    Retrieves current weather and temperature for a given location to help determine travel seasonality.
    Args:
        location: The city or region name (e.g., 'Tokyo', 'Karnal').
    """
    try:
        # Step 1: Geocode the location (Open-Meteo geocoding API)
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={location}&count=1&format=json"
        geo_data = requests.get(geo_url).json()
        
        if not geo_data.get("results"):
            return f"Could not find weather data for {location}."
            
        lat = geo_data["results"][0]["latitude"]
        lon = geo_data["results"][0]["longitude"]
        
        # Step 2: Get the weather
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        weather_data = requests.get(weather_url).json()
        
        current = weather_data["current_weather"]
        temp = current["temperature"]
        return f"The current temperature in {location} is {temp}°C. Use this to advise on packing and seasonality."
    except Exception as e:
        return f"Weather service unavailable: {str(e)}"

def convert_currency(amount: float, from_currency: str, to_currency: str) -> str:
    """
    Converts a budget amount from one currency to another using current market rates.
    Args:
        amount: The numerical amount to convert.
        from_currency: The 3-letter currency code to convert from (e.g., 'INR', 'USD').
        to_currency: The 3-letter currency code to convert to (e.g., 'EUR', 'JPY').
    """
    # Note: In a production app, replace this URL with a real API like ExchangeRate-API or Frankfurter
    try:
        url = f"https://api.frankfurter.app/latest?amount={amount}&from={from_currency}&to={to_currency}"
        response = requests.get(url).json()
        if "rates" in response:
            converted = response["rates"][to_currency]
            return f"{amount} {from_currency} is currently equal to {converted} {to_currency}."
        return "Currency conversion failed."
    except Exception as e:
         return f"Currency service unavailable: {str(e)}"