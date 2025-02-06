
import pytest
from unittest.mock import MagicMock
from utils.geo_util_meteo import GeoDataUtil
from back.geo_service import GeoService

"""
	run with  python3 -m pytest tests/test_geo_service.py
"""

@pytest.fixture
def mock_geo_util():
    """
    Mock the GeoDataUtil class.
    """
    return MagicMock()


@pytest.fixture
def geo_service(mock_geo_util):
    """
    Create an instance of GeoService with the mocked GeoDataUtil.
    """
    geo_service = GeoService()
    geo_service.geo_util = mock_geo_util  
    return geo_service


def test_get_location_valid_data(geo_service, mock_geo_util):
    """
    Test get_location with valid data.
    """
    
    mock_geo_util.fetch_geo_data.return_value = [
        {
            "lat": 32.0625,
            "lon": 34.8125,
            "name": "Tel Aviv",
            "country": "Israel"
        }
    ]

    location = geo_service.get_location("Tel Aviv", "Israel")

    assert location is not None, "Location should not be None"
    assert location["lat"] == 32.0625, "Latitude is incorrect"
    assert location["lon"] == 34.8125, "Longitude is incorrect"
    assert location["name"] == "Tel Aviv", "City name is incorrect"
    assert location["country"] == "Israel", "Country name is incorrect"

    mock_geo_util.fetch_geo_data.assert_called_once_with("Tel Aviv", "Israel")


def test_get_location_no_data(geo_service, mock_geo_util):
    """
    Test get_location with no data returned.
    """
    mock_geo_util.fetch_geo_data.return_value = []

    location = geo_service.get_location("Unknown City", "Unknown Country")

    assert location is None, "Location should be None when no data is returned"

    mock_geo_util.fetch_geo_data.assert_called_once_with("Unknown City", "Unknown Country")


def test_get_location_invalid_data(geo_service, mock_geo_util):
    """
    Test get_location with invalid data (not a list).
    """
    mock_geo_util.fetch_geo_data.return_value = None

    location = geo_service.get_location("Invalid City", "Invalid Country")

    assert location is None, "Location should be None when invalid data is returned"

    mock_geo_util.fetch_geo_data.assert_called_once_with("Invalid City", "Invalid Country")

