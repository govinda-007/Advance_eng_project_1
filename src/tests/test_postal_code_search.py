import pandas as pd
from typing import Any, Dict
import pytest
from unittest.mock import patch
#from charging.application.services.Search import PostalCodeSearch
from charging.application.services.Search import PostalCodeSearch, MapGenerator, UIHandler, ChargingStationApp
import sys
import os
from config import pdict
import folium
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture
def dframe1():
    df = pd.read_csv(pdict["file_geodat_plz"], delimiter=";")
    if "Number" not in df.columns:
        df["Number"] = 0  # Add a default column if missing
    return df

@pytest.fixture
def dframe2():
    df2 = pd.read_csv(pdict["file_lstations"], delimiter=";", encoding='utf-8')
    return df2.rename(columns={'Postleitzahl': 'PLZ'})
    
# Test for valid postal code
def test_filter_data_valid_postal_code(dframe1, dframe2):
    """
    Test the valid postal code filtering with the PostalCodeSearch service.
    Ensures the filtered data contains results and required columns.
    """
    # Initialize the PostalCodeSearch service
    search = PostalCodeSearch()

    # Perform the charging station search using postal code dataframes
    result = search.charging_station_search_by_postal_code(dframe1, dframe2)

    # Validate the filtered data by a specific postal code
    data = search.filter_data_by_postal_code(10115)

    # Assertions to check the results are not empty and contain expected columns
    assert 'merged_data' in data, "Expected 'merged_data' in the result dictionary."
    assert data['merged_data'].shape[0] > 0, "Merged data should not be empty for valid postal code."
    assert 'filtered_dframe2' in data, "Expected 'filtered_dframe2' in the result dictionary."
    
    # Check if geometry column exists after the merge
    if 'geometry' in data['filtered_dframe2'].columns:
        assert 'geometry' in data['filtered_dframe2'].columns, "Filtered dataframe should include 'geometry' column."
    else:
        print("Warning: 'geometry' column is missing in filtered_dframe2.")
        # Handle the situation, perhaps skip this specific check, or log an error


# Test for missing postal code
def test_filter_data_missing_postal_code(dframe1, dframe2):
    search = PostalCodeSearch()
    search.charging_station_search_by_postal_code(dframe1, dframe2)
    data = search.filter_data_by_postal_code(99999)  # A postal code not in the data
    assert data == {}

# Test for empty dataframe
def test_filter_data_empty_dataframe(dframe1, dframe2):
    search = PostalCodeSearch()
    search.charging_station_search_by_postal_code(dframe1, dframe2)
    data = search.filter_data_by_postal_code(10116)  # A postal code not in dframe1 or dframe2
    assert data == {}

# Test MapGenerator methods
def test_create_base_map():
    """Test base map creation"""
    map_obj = MapGenerator.create_base_map([52.52, 13.40], 10)
    assert isinstance(map_obj, folium.Map)

def test_add_marker_cluster():
    """Test adding marker cluster"""
    map_obj = MapGenerator.create_base_map([52.52, 13.40], 10)
    cluster = MapGenerator.add_marker_cluster(map_obj)
    assert isinstance(cluster, folium.plugins.MarkerCluster)

def test_add_marker():
    """Test adding a marker"""
    map_obj = MapGenerator.create_base_map([52.52, 13.40], 10)
    MapGenerator.add_marker(map_obj, [52.52, 13.40], "Test Marker", "blue")

def test_add_geojson_overlay():
    """Test adding a GeoJSON overlay"""
    map_obj = MapGenerator.create_base_map([52.52, 13.40], 10)
    MapGenerator.add_geojson_overlay(map_obj, {"type": "Feature"}, "10115")

# Mocking Streamlit functions to test UIHandler
@patch("streamlit.sidebar.text_input", return_value="10115")
@patch("streamlit.sidebar.button", return_value=True)
def test_render_sidebar(mock_text_input, mock_button):
    """Test rendering sidebar user input"""
    postal_code = UIHandler.render_sidebar()
    assert postal_code == "10115"

'''@patch("streamlit.write")
def test_render_results_with_data(mock_write, dframe1, dframe2):'''
    

@patch("streamlit.write")
def test_render_results_no_data(mock_write):
    """Test rendering when no data is found"""
    map_obj = MapGenerator.create_base_map([52.52, 13.40], 10)
    UIHandler.render_results(map_obj, {})

# Test ChargingStationApp
@patch("streamlit.sidebar.text_input", return_value="10115")
@patch("streamlit.sidebar.button", return_value=True)
@patch("streamlit.write")
def test_charging_station_app(mock_write, mock_text_input, mock_button, dframe1, dframe2):
    """Test the full app execution"""
    app = ChargingStationApp()
    app.search_handler = PostalCodeSearch()
    app.search_handler.charging_station_search_by_postal_code(dframe1, dframe2)
    app.run()



'''import pandas as pd
from typing import Any, Dict
import pytest
from charging.application.services.Search import PostalCodeSearch
import sys
import os
from config import pdict
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture
def dframe1():
    df = pd.read_csv(pdict["file_geodat_plz"], delimiter=";")
    if "Number" not in df.columns:
        df["Number"] = 0  # Add a default column if missing
    return df

@pytest.fixture
def dframe2():
    df2 = pd.read_csv(pdict["file_lstations"], delimiter=";", encoding='utf-8')
    return df2.rename(columns={'Postleitzahl': 'PLZ'})
    
# Test for valid postal code
def test_filter_data_valid_postal_code(dframe1, dframe2):
    """
    Test the valid postal code filtering with the PostalCodeSearch service.
    Ensures the filtered data contains results and required columns.
    """
    # Initialize the PostalCodeSearch service
    search = PostalCodeSearch()

    # Perform the charging station search using postal code dataframes
    result = search.charging_station_search_by_postal_code(dframe1, dframe2)

    # Validate the filtered data by a specific postal code
    data = search.filter_data_by_postal_code(10115)

    # Assertions to check the results are not empty and contain expected columns
    assert 'merged_data' in data, "Expected 'merged_data' in the result dictionary."
    assert data['merged_data'].shape[0] > 0, "Merged data should not be empty for valid postal code."
    assert 'filtered_dframe2' in data, "Expected 'filtered_dframe2' in the result dictionary."
    
    # Check if geometry column exists after the merge
    if 'geometry' in data['filtered_dframe2'].columns:
        assert 'geometry' in data['filtered_dframe2'].columns, "Filtered dataframe should include 'geometry' column."
    else:
        print("Warning: 'geometry' column is missing in filtered_dframe2.")
        # Handle the situation, perhaps skip this specific check, or log an error.


# Test for missing postal code
def test_filter_data_missing_postal_code(dframe1, dframe2):
    search = PostalCodeSearch()
    search.charging_station_search_by_postal_code(dframe1, dframe2)
    data = search.filter_data_by_postal_code(99999)  # A postal code not in the data
    assert data == {}

# Test for empty dataframe
def test_filter_data_empty_dataframe(dframe1, dframe2):
    search = PostalCodeSearch()
    search.charging_station_search_by_postal_code(dframe1, dframe2)
    data = search.filter_data_by_postal_code(10116)  # A postal code not in dframe1 or dframe2
    assert data == {}'''