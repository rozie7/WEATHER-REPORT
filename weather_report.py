"""
Weather Report for Nairobi, Kenya for the next 3 days using Open-Meteo API.
Branch: feature/weather-api

"""

import requests

CITY_NAME = "Nairobi, Kenya"
 
API_URL = "https://api.open-meteo.com/v1/forecast?latitude=-1.2833&longitude=36.8167&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max&hourly=temperature_2m,relative_humidity_2m,precipitation_probability,weather_code,wind_speed_10m&timezone=Africa%2FCairo&forecast_days=3&wind_speed_unit=ms"
# This is the API URL copied from the Open-Meteo website

def get_forecast():
    """Ask Open-Meteo for the forecast and return it as a dictionary."""
    response = requests.get(API_URL, timeout=10)

    # Converts the JSON text from the API into a Python dictionary
    return response.json()


def main():
    """Get the forecast and print a simple summary to test it."""
    # Stop with a friendly message if the URL was not pasted in
    if "PASTE_YOUR" in API_URL:
        print("Please paste your Open-Meteo URL into API_URL first.")
        return

    data = get_forecast()
    daily = data["daily"]

    print(f"City: {CITY_NAME}")
    print(f"Forecast days received: {len(daily['time'])}")

    # Loop through each day and print its values
    for i in range(len(daily["time"])):
        print(
            f"{daily['time'][i]} | weather code: {daily['weather_code'][i]} | "
            f"min: {daily['temperature_2m_min'][i]} | "
            f"max: {daily['temperature_2m_max'][i]} | "
            f"rain chance: {daily['precipitation_probability_max'][i]}%"
        )

    print(f"Hourly values received: {len(data['hourly']['time'])}")

if __name__ == "__main__":
    main()