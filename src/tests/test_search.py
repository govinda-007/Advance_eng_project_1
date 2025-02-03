import pytest
from unittest.mock import MagicMock
import pandas as pd
from charging.application.services.Search import SearchService


@pytest.fixture
def mock_df_lstat():
    """Create a mock DataFrame for testing"""
    data = {
        "Postleitzahl": [10115, 10117, 10119],
        "Anzeigename (Karte)": ["Station A", "Station B", "Station C"],
        "Breitengrad": [52.5200, 52.5250, 52.5300],
        "Längengrad": [13.4050, 13.4100, 13.4150]
    }
    return pd.DataFrame(data)


@pytest.fixture
def search_service(mock_df_lstat):
    """Create an instance of SearchService"""
    return SearchService(mock_df_lstat)


def test_search_by_postal_code_valid(search_service, mock_df_lstat):
    """Test searching for a valid postal code that exists"""
    postal_code = "10115"  # A postal code in the mock DataFrame
    expected_stations = [
        {"name": "Station A", "status": "Available", "location": (52.5200, 13.4050)}
    ]
    
    result = search_service.search_by_postal_code(postal_code)
    
    assert result == expected_stations, f"Expected {expected_stations}, but got {result}"


def test_search_by_postal_code_invalid(search_service):
    """Test searching for an invalid postal code"""
    postal_code = "99999"  # A postal code that doesn't exist in the mock DataFrame
    expected_result = []  # No stations should match
    
    result = search_service.search_by_postal_code(postal_code)
    
    assert result == expected_result, f"Expected {expected_result}, but got {result}"


def test_search_invalid_postal_code_format(search_service):
    """Test searching for a postal code with an invalid format"""
    postal_code = "invalid_code"  # Invalid postal code format
    expected_result = []  # Invalid format should result in an empty list
    
    result = search_service.search_by_postal_code(postal_code)
    
    assert result == expected_result, f"Expected {expected_result}, but got {result}"


def test_search_empty_dataframe(search_service):
    """Test searching when the DataFrame is empty"""
    empty_df = pd.DataFrame(columns=["Postleitzahl", "Anzeigename (Karte)", "Breitengrad", "Längengrad"])
    search_service.df_lstat = empty_df  # Set the service to use the empty DataFrame
    postal_code = "10115"
    expected_result = []  # No data in the DataFrame, so no results
    
    result = search_service.search_by_postal_code(postal_code)
    
    assert result == expected_result, f"Expected {expected_result}, but got {result}"


def test_search_with_invalid_coordinates(search_service, mock_df_lstat):
    """Test handling of invalid coordinates in the DataFrame"""
    # Modify the DataFrame to include invalid coordinates
    mock_df_lstat.at[0, "Breitengrad"] = "invalid_lat"
    mock_df_lstat.at[0, "Längengrad"] = "invalid_lon"
    
    postal_code = "10115"
    expected_result = []  # Invalid coordinates should result in no valid stations
    
    result = search_service.search_by_postal_code(postal_code)
    
    assert result == expected_result, f"Expected {expected_result}, but got {result}"
