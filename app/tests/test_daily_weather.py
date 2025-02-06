import datetime as dt

class Weather(object):
    def __init__(self, night_temp, day_temp, humidity):
        self.night_temp = night_temp 
        self.day_temp = day_temp 
        self.humidity = humidity
        self.timestamp = dt.datetime.now()

# Extract and process data
data = {
    "latitude": 32.0625,
    "longitude": 34.8125,
    "generationtime_ms": 0.033855438232421875,
    "utc_offset_seconds": 7200,
    "timezone": "Asia/Jerusalem",
    "timezone_abbreviation": "GMT+2",
    "elevation": 17.0,
    "hourly_units": {"time": "iso8601", "relative_humidity_2m": "%"},
    "hourly": {
        "time": [
            "2025-01-16T00:00", "2025-01-16T01:00", "2025-01-16T02:00", 
            # Shortened for brevity
        ],
        "relative_humidity_2m": [
            91, 91, 91, 91, 90, 89, 89, 89, 87, 
            # Shortened for brevity
        ],
    },
    "daily_units": {
        "time": "iso8601",
        "temperature_2m_max": "°C",
        "temperature_2m_min": "°C"
    },
    "daily": {
        "time": ["2025-01-16", "2025-01-17", "2025-01-18", "2025-01-19", 
                 "2025-01-20", "2025-01-21", "2025-01-22"],
        "temperature_2m_max": [20.0, 19.7, 19.2, 19.3, 19.6, 22.3, 20.9],
        "temperature_2m_min": [13.0, 12.8, 11.0, 11.8, 10.7, 11.4, 15.5],
    }
}

# Calculate average humidity
hourly_humidity = data["hourly"]["relative_humidity_2m"]
average_humidity = sum(hourly_humidity) / len(hourly_humidity)

# Get the first day's min/max temps as an example
night_temp = data["daily"]["temperature_2m_min"][0]
day_temp = data["daily"]["temperature_2m_max"][0]

# Create a Weather instance
weather = Weather(night_temp, day_temp, average_humidity)

# Display the Weather instance
print(f"Night Temp: {weather.night_temp}°C")
print(f"Day Temp: {weather.day_temp}°C")
print(f"Average Humidity: {weather.humidity:.2f}%")
print(f"Timestamp: {weather.timestamp}")

