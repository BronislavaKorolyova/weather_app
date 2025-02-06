import pytest
from unittest.mock import patch, MagicMock
from back.models.week_weather import WeekWeather
from back.weather_service import WeatherService

"""
	run with  python3 -m pytest tests/test_weather_service.py
"""

@pytest.fixture
def weather_service():
    return WeatherService()


@pytest.fixture
def mock_weather_data():
    return {
        "daily": {
            "time": ["2025-01-16", "2025-01-17", "2025-01-18"],
            "temperature_2m_min": [13.0, 12.8, 11.0],
            "temperature_2m_max": [20.0, 19.7, 19.2],
            "weathercode": [3,2,3,80,80,80,2]
        },
        "hourly": {
            "relative_humidity_2m": [
                90, 91, 92, 90, 89, 88, 87, 86, 85, 84, 83, 82, 81, 80, 79, 78, 77, 76, 75, 74, 73, 72, 71, 70,
                69, 68, 67, 66, 65, 64, 63, 62, 61, 60, 59, 58, 57, 56, 55, 54, 53, 52, 51, 50, 49, 48, 47, 46,
                45, 44, 43, 42, 41, 40, 39, 38, 37, 36, 35, 34, 33, 32, 31, 30, 29, 28, 27, 26, 25, 24, 23, 22
            ] * 3  
        }
    }


def test_calculate_daily_humidity(weather_service):
    hourly_humidity = [90] * 24 + [80] * 24 + [70] * 24
    num_days = 3

    result = weather_service._calculate_daily_humidity(hourly_humidity, num_days)

    assert result == [90.0, 80.0, 70.0], "Daily humidity calculation is incorrect"


@patch("back.weather_service.requests.get")
def test_get_weather_data(mock_get, weather_service, mock_weather_data):
    mock_response = MagicMock()
    mock_response.json.return_value = mock_weather_data
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    city = "Tel Aviv"
    country = "Israel"
    latitude = 32.0625
    longitude = 34.8125

    week_weather = weather_service.get_weather_data(latitude, longitude, city, country)

    assert isinstance(week_weather, WeekWeather), "Returned object is not a WeekWeather instance"
    assert week_weather.city == city, "City name is incorrect in WeekWeather"
    assert week_weather.country == country, "Country name is incorrect in WeekWeather"
    assert len(week_weather.days) == 3, "Incorrect number of days in WeekWeather"

    first_day = week_weather.days[0]
    assert first_day.date == "16/01/2025", "Incorrect date for the first day"
    assert first_day.night_temp == 13.0, "Incorrect night temperature for the first day"
    assert first_day.day_temp == 20.0, "Incorrect day temperature for the first day"
    assert first_day.humidity == 81.38, "Incorrect humidity for the first day"


def test_process_weather_data(weather_service, mock_weather_data):
    city = "Tel Aviv"
    country = "Israel"

    week_weather = weather_service._process_weather_data(mock_weather_data, city, country)

    assert isinstance(week_weather, WeekWeather), "Returned object is not a WeekWeather instance"
    assert week_weather.city == city, "City name is incorrect in WeekWeather"
    assert week_weather.country == country, "Country name is incorrect in WeekWeather"
    assert len(week_weather.days) == 3, "Incorrect number of days in WeekWeather"

    first_day = week_weather.days[0]
    assert first_day.date == "16/01/2025", "Incorrect date for the first day"
    assert first_day.night_temp == 13.0, "Incorrect night temperature for the first day"
    assert first_day.day_temp == 20.0, "Incorrect day temperature for the first day"
    assert first_day.humidity == 81.38, "Incorrect humidity for the first day"

