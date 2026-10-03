# Weather Report

A beginner Python program that shows a 3-day weather forecast for **Nairobi, Kenya**, using the free [Open-Meteo](https://open-meteo.com) API. No API key is needed.

## What the program shows

For each of the next 3 days (today, tomorrow, the day after tomorrow):

- The date
- Readings at **06:00** and **15:00**: weather condition, temperature, rain chance, humidity and wind speed
- A daily summary: weather condition, minimum and maximum temperature, and the highest rain chance

The data is a real forecast downloaded from Open-Meteo every time you run the program.

## Requirements

- Python 3.8 or newer
- The `requests` library
- An internet connection

## How to run

1. Download or clone this repository:
```
   git clone https://github.com/rozie7/WEATHER-REPORT.git
```
2. Open the `WEATHER-REPORT` folder in a terminal (for example, in VS Code).
3. Install the library:
```
   python -m pip install requests
```
4. Run the program:
```
   python weather_report.py
```

## Example output

This is the start of a real run on 3 October 2026 (your numbers will differ, because the forecast changes):

```
==================================================
Weather forecast for Nairobi, Kenya
Data source: Open-Meteo API (06:00 and 15:00 readings)
==================================================

Today (Sat 03 Oct)
--------------------------------------------------
  Morning (06:00)
    Weather:     Clear sky
    Temperature: 14.6 °C
    Rain chance: 0%
    Humidity:    86%
    Wind speed:  1.57 m/s
```

## How it works

1. `get_forecast()` sends a request to the Open-Meteo forecast API (`https://api.open-meteo.com/v1/forecast`) using the `requests` library and receives the forecast as JSON.
2. `describe_weather()` turns Open-Meteo's numeric weather codes (WMO codes) into readable words such as "Overcast".
3. `print_report()` and `print_time_slot()` format the data into the report.
4. `main()` runs everything and shows a friendly message if something goes wrong.

The API address in `weather_report.py` was created on the Open-Meteo documentation page. It contains Nairobi's coordinates (latitude -1.2921, longitude 36.8219), the weather variables we use, the Africa/Nairobi timezone, wind speed in m/s, and 3 forecast days.

## Error handling

The program does not crash with a long error message. It prints a short explanation if:

- there is no internet connection
- the weather server takes too long to answer (10-second limit)
- the server reports an error
- the data is in an unexpected format or is incomplete

## Troubleshooting

| Problem | What to try |
|---|---|
| `ModuleNotFoundError: No module named 'requests'` | Run `python -m pip install requests` |
| `Error: Could not connect to the internet.` | Check your connection and run again |
| `'python' is not recognized` | Install Python from python.org and tick "Add Python to PATH" |
| Weather says "Unknown" | The weather code is not in the `WEATHER_CODES` dictionary; add it there |
| The `°` symbol looks garbled | Use a terminal that supports UTF-8, such as the VS Code terminal |

## Project structure

```
WEATHER-REPORT/
├── weather_report.py          # the program
├── README.md                  # this file
├── github project address.txt # the GitHub project URL
└── captures/               # screenshots of Git and GitHub work
```

## Git workflow

The project was built with five feature branches, each merged into `main` through a pull request:

| Branch | Purpose |
|---|---|
| `feature/weather-api` | Get the forecast data from Open-Meteo |
| `feature/weather-display` | Format and display the weather report |
| `feature/error-handling` | Handle network and API errors |
| `feature/documentation` | Write this README |
| `feature/project-polish` | Final output improvements and checks |

## Credits

Weather data by [Open-Meteo.com](https://open-meteo.com/), used under their free non-commercial terms.