#Project link: https://github.com/rozie7/WEATHER-REPORT
"""
Shows a 3-day forecast (06:00 and 15:00 readings plus a daily summary)
using real data from the free Open-Meteo API.

"""

import requests
from datetime import datetime

CITY_NAME = "Nairobi, Kenya"
 
API_URL = "https://api.open-meteo.com/v1/forecast?latitude=-1.2833&longitude=36.8167&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max&hourly=temperature_2m,relative_humidity_2m,precipitation_probability,weather_code,wind_speed_10m&timezone=Africa%2FCairo&forecast_days=3&wind_speed_unit=ms"
# This is the API URL copied from the Open-Meteo website

def get_forecast():
    """Ask Open-Meteo for the forecast.
    Returns a dictionary, or None if something went wrong."""
    # "try" runs the risky code. If it fails, Python jumps to "except"
    # if the request fails, we catch the exception and print a message instead of crashing
    try:
        # Send the request and wait up to 10 seconds
        response = requests.get(API_URL, timeout=10)
        # Raise an error if the server answered with a failure code (404, 500...)
        response.raise_for_status()
        # Convert the JSON text into a Python dictionary
        data = response.json()
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the internet.")
        print("Please check your connection and try again.")
        return None
    except requests.exceptions.Timeout:
        print("Error: The weather server took too long to answer.")
        print("Please try again in a moment.")
        return None
    except requests.exceptions.HTTPError as error:
        print(f"Error: The weather server reported a problem ({error}).")
        return None
    except ValueError:
        # Happens when the answer is not valid JSON
        print("Error: The weather server sent data in an unexpected format.")
        return None
    except requests.exceptions.RequestException as error:
        # Catches any other request problem
        print(f"Error: The request failed ({error}).")
        return None

    # Open-Meteo can report a problem inside the data with "error": true
    if isinstance(data, dict) and data.get("error"):
        print(f"Error from the weather API: {data.get('reason', 'unknown reason')}")
        return None

    # Make sure the parts of the forecast we need are present
    for section in ("daily", "hourly"):
        if section not in data:
            print(f"Error: The forecast is missing its '{section}' data.")
            return None

    return data


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
    print("All times are Nairobi local time (GMT+3)")
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

    print("Forecast data provided by Open-Meteo.com")

def main():
    """Get the forecast and print the report."""
    # Stop with a friendly message if the URL was not pasted in
    if "PASTE_YOUR" in API_URL:
        print("Please paste your Open-Meteo URL into API_URL first.")
        return

    data = get_forecast()

    if data is None:
        print("The weather report could not be shown.")
        return

    try:
        print_report(data)
    except (KeyError, ValueError, IndexError, TypeError):
        # Happens if the forecast has missing or unexpected values
        print("Error: The forecast data was incomplete, "
              "so the report could not be shown.")

if __name__ == "__main__":
    main()