import folium
from folium.plugins import MarkerCluster
import streamlit as st
from streamlit_folium import folium_static
from branca.colormap import LinearColormap
from typing import Any, Dict, List
import pandas as pd


# Single Responsibility Principle (SRP): 
# Each class has one responsibility: map generation, postal code searching, UI handling.

# Map Generation Class - Responsible only for map-related logic.
class MapGenerator:
    """Handles map creation and marker addition"""

    def create_base_map(self, center: List[float], zoom: int) -> folium.Map:
        """Create a base map centered at a location"""
        return folium.Map(location=center, zoom_start=zoom)

    def add_marker_cluster(self, map_object: folium.Map) -> MarkerCluster:
        """Add a marker cluster to the map"""
        return MarkerCluster().add_to(map_object)

    def add_geojson_overlay(self, map_object: folium.Map, geometry: Any, postal_code: str) -> None:
        """Add a GeoJSON overlay to highlight a region"""
        folium.GeoJson(
            data=geometry,
            style_function=lambda x: {
                'fillColor': 'yellow',
                'color': 'black',
                'weight': 2,
                'fillOpacity': 0.5
            },
            tooltip=f"PLZ: {postal_code}"
        ).add_to(map_object)

    def add_marker(self, map_object: folium.Map, location: List[float], popup: str, icon_color: str) -> None:
        """Add a marker to the map"""
        folium.Marker(
            location=location,
            popup=popup,
            icon=folium.Icon(color=icon_color)
        ).add_to(map_object)


# Open/Closed Principle (OCP):
# The PostalCodeSearch class is now open for extension by allowing custom data filtering logic.
class PostalCodeSearch:
    """Handles postal code search logic"""

    def __init__(self, dframe1: pd.DataFrame, dframe2: pd.DataFrame):
        self.dframe1 = dframe1
        self.dframe2 = dframe2

    def filter_data_by_postal_code(self, postal_code: int) -> Dict[str, Any]:
        """Filter data by postal code and return results"""
        filtered_dframe1 = self.dframe1[self.dframe1['PLZ'] == postal_code]
        filtered_dframe2 = self.dframe2[self.dframe2['PLZ'] == postal_code]
        if filtered_dframe1.empty or filtered_dframe2.empty:
            return {}

        merged_data = filtered_dframe2.merge(
            filtered_dframe1[['PLZ', 'Number']],
            on='PLZ',
            how='left'
        )
        return {
            "merged_data": merged_data,
            "filtered_dframe2": filtered_dframe2
        }


# Interface Segregation Principle (ISP):
# Clients only need to interact with specific methods for the features they need. Here, UI is isolated.
class UIHandler:
    """Handles user interface rendering"""

    def render_sidebar(self) -> str:
        """Render sidebar for user input"""
        st.sidebar.markdown("### Search Charging Stations by Postal Code")
        postal_code = st.sidebar.text_input("Enter Postal Code (PLZ)", "")
        search_button = st.sidebar.button("Search")
        return postal_code if search_button else ""

    def render_results(self, map_object: folium.Map, data: Dict[str, Any]) -> None:
        """Render the search results on the map and in the UI"""
        if data:
            map_generator = MapGenerator()
            marker_cluster = map_generator.add_marker_cluster(map_object)
            for _, row in data["merged_data"].iterrows():
                st.subheader(f"Postal Code: {row['PLZ']}")
                st.subheader(f"Available Stations: {row['Number']}")
                map_generator.add_marker(
                    map_object,
                    location=[float(row['Breitengrad']), float(row['Längengrad'])],
                    popup=f"PIN: {row['PLZ']}, Number: {row['Number']}",
                    icon_color='green'
                )

            for _, row in data["filtered_dframe2"].iterrows():
                map_generator.add_geojson_overlay(map_object, row['geometry'], row['PLZ'])

            folium_static(map_object, width=800, height=600)
        else:
            st.write("No charging stations found for this postal code.")


# Dependency Inversion Principle (DIP):
# High-level module (UIHandler) is not dependent on low-level module (PostalCodeSearch). Both depend on abstractions.

class ChargingStationApp:
    """Main application to search for charging stations"""

    def __init__(self, map_generator: MapGenerator, ui_handler: UIHandler, postal_code_search: PostalCodeSearch):
        self.map_generator = map_generator
        self.ui_handler = ui_handler
        self.postal_code_search = postal_code_search

    def run(self) -> None:
        """Run the application"""
        map_center = [52.52, 13.40]  # Berlin center
        map_object = self.map_generator.create_base_map(map_center, 10)
        postal_code = self.ui_handler.render_sidebar()

        if postal_code:
            try:
                postal_code = int(postal_code)
                data = self.postal_code_search.filter_data_by_postal_code(postal_code)
                self.ui_handler.render_results(map_object, data)
            except ValueError:
                st.write("Please enter a valid postal code.")
        else:
            st.write("Enter a postal code and click 'Search' to find charging stations.")
