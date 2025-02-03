import pytest
import folium
import pandas as pd
import geopandas as gpd
from shapely.geometry import Polygon, Point
from charging.application.services.Visualize import Visualize

@pytest.fixture
def sample_residents_data():
    """Create a sample GeoDataFrame with valid geometries for residents"""
    data = {
        'PLZ': [10115, 10117, 10119],
        'Einwohner': [5000, 7000, 6000],
        'geometry': [
            Polygon([(13.4, 52.5), (13.5, 52.5), (13.5, 52.6), (13.4, 52.6)]),
            Polygon([(13.5, 52.5), (13.6, 52.5), (13.6, 52.6), (13.5, 52.6)]),
            Polygon([(13.6, 52.5), (13.7, 52.5), (13.7, 52.6), (13.6, 52.6)])
        ]
    }
    return gpd.GeoDataFrame(data, crs="EPSG:4326")  # Set the correct CRS

@pytest.fixture
def sample_charging_stations_data():
    """Create a sample GeoDataFrame with valid geometries for charging stations"""
    data = {
        'PLZ': [10115, 10117, 10119],
        'Number': [5, 10, 7],
        'geometry': [
            Point(13.4, 52.5),
            Point(13.5, 52.5),
            Point(13.6, 52.5)
        ]
    }
    return gpd.GeoDataFrame(data, crs="EPSG:4326")  # Set the correct CRS

@pytest.fixture
def visualize_instance():
    """Fixture to create an instance of Visualize"""
    return Visualize()

def test_render_map_residents(visualize_instance, sample_residents_data, sample_charging_stations_data):
    """Test if render_map correctly calls _render_residents_layer"""
    try:
        visualize_instance.render_map(sample_charging_stations_data, sample_residents_data, "Residents")
        assert True
    except Exception as e:
        pytest.fail(f"render_map failed for Residents layer: {e}")

def test_render_map_charging_stations(visualize_instance, sample_residents_data, sample_charging_stations_data):
    """Test if render_map correctly calls _render_charging_stations_layer"""
    try:
        visualize_instance.render_map(sample_charging_stations_data, sample_residents_data, "Charging_Stations")
        assert True
    except Exception as e:
        pytest.fail(f"render_map failed for Charging_Stations layer: {e}")

def test_render_residents_layer(visualize_instance, sample_residents_data):
    """Test if _render_residents_layer runs without errors"""
    try:
        visualize_instance._render_residents_layer(sample_residents_data)
        assert True
    except Exception as e:
        pytest.fail(f"_render_residents_layer failed: {e}")

def test_render_charging_stations_layer(visualize_instance, sample_charging_stations_data):
    """Test if _render_charging_stations_layer runs without errors"""
    try:
        visualize_instance._render_charging_stations_layer(sample_charging_stations_data)
        assert True
    except Exception as e:
        pytest.fail(f"_render_charging_stations_layer failed: {e}")
