"""
Weather Report for Nairobi, Kenya for the next 3 days using Open-Meteo API.
Branch: feature/weather-api

"""

import requests
from datetime import datetime

CITY_NAME = "Nairobi, Kenya"
 
API_URL = "https://api.open-meteo.com/v1/forecast?latitude=-1.2833&longitude=36.8167&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max&hourly=temperature_2m,relative_humidity_2m,precipitation_probability,weather_code,wind_speed_10m&timezone=Africa%2FCairo&forecast_days=3&wind_speed_unit=ms"
# This is the API URL copied from the Open-Meteo website

def get_forecast():
    """Ask Open-Meteo for the forecast and return it as a dictionary."""
    response = requests.get(API_URL, timeout=10)

    # Converts the JSON text from the API into a Python dictionary
    return response.json()


# Weather codes are numbers from the WMO standard.
# This dictionary turns each number into words.
WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}


def describe_weather(code):
    """Return the words for a weather code (or 'Unknown' if not in the list)."""
    return WEATHER_CODES.get(int(code), "Unknown")


def print_time_slot(hourly, date, hour, label):
    """Print the weather for one hour (for example 06:00) of one day."""
    # Hourly times look like "2026-10-03T06:00", so build that string to find the right position in the lists
    key = f"{date}T{hour:02d}:00"
    i = hourly["time"].index(key)  # position of that hour in the lists

    print(f"  {label} ({hour:02d}:00)")
    print(f"    Weather:     {describe_weather(hourly['weather_code'][i])}")
    print(f"    Temperature: {hourly['temperature_2m'][i]} °C")
    print(f"    Rain chance: {hourly['precipitation_probability'][i]}%")
    print(f"    Humidity:    {hourly['relative_humidity_2m'][i]}%")
    print(f"    Wind speed:  {hourly['wind_speed_10m'][i]} m/s")
    print()


def print_report(data):
    """Print the full 3-day weather report."""
    daily = data["daily"]
    hourly = data["hourly"]
    day_names = ["Today", "Tomorrow", "Day after tomorrow"]
    thick_line = "=" * 50
    thin_line = "-" * 50

    print(thick_line)
    print(f"Weather forecast for {CITY_NAME}")
    print("Data source: Open-Meteo API (06:00 and 15:00 readings)")
    print(thick_line)

    # Go through each day one by one
    for i in range(len(daily["time"])):
        date = daily["time"][i]  # for example "2026-10-03"
        # Turn "2026-10-03" into a better text like "Sat 03 Oct"
        nice_date = datetime.strptime(date, "%Y-%m-%d").strftime("%a %d %b")

        print()
        print(f"{day_names[i]} ({nice_date})")
        print(thin_line)

        print_time_slot(hourly, date, 6, "Morning")
        print_time_slot(hourly, date, 15, "Afternoon")

        # Daily summary from the "daily" part of the data
        print(f"  Day summary: {describe_weather(daily['weather_code'][i])}")
        print(f"  Temperature: min {daily['temperature_2m_min'][i]} °C / "
              f"max {daily['temperature_2m_max'][i]} °C")
        print(f"  Highest rain chance: "
              f"{daily['precipitation_probability_max'][i]}%")
        print()
        print(thick_line)


def main():
    """Get the forecast and print the report."""
    if "PASTE_YOUR" in API_URL:
        print("Please paste your Open-Meteo URL into API_URL first.")
        return

    data = get_forecast()
    print_report(data)

if __name__ == "__main__":
    main()