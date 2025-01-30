import folium
from folium.plugins import MarkerCluster
import streamlit as st
from streamlit_folium import folium_static
from branca.colormap import LinearColormap
from typing import Any, Dict, List
import logging

# SOLID Refactor

class MapGenerator:
    """Handles map creation and marker addition"""

    @staticmethod
    def create_base_map(center: List[float], zoom: int) -> folium.Map:
        """Create a base map centered at a location"""
        return folium.Map(location=center, zoom_start=zoom)

    @staticmethod
    def add_marker_cluster(map_object: folium.Map) -> MarkerCluster:
        """Add a marker cluster to the map"""
        return MarkerCluster().add_to(map_object)

    @staticmethod
    def add_geojson_overlay(map_object: folium.Map, geometry: Any, postal_code: str) -> None:
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

    @staticmethod
    def add_marker(map_object: folium.Map, location: List[float], popup: str, icon_color: str) -> None:
        """Add a marker to the map"""
        folium.Marker(
            location=location,
            popup=popup,
            icon=folium.Icon(color=icon_color)
        ).add_to(map_object)


class PostalCodeSearch:
    """Handles postal code search logic"""

    def charging_station_search_by_postal_code(self, dframe1, dframe2):
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


class UIHandler:
    """Handles user interface rendering"""

    @staticmethod
    def render_sidebar() -> str:
        """Render sidebar for user input"""
        st.sidebar.markdown("### Search Charging Stations by Postal Code")
        postal_code = st.sidebar.text_input("Enter Postal Code (PLZ)", "")
        search_button = st.sidebar.button("Search")
        return postal_code if search_button else ""

    @staticmethod
    def render_results(map_object: folium.Map, data: Dict[str, Any]) -> None:
        """Render the search results on the map and in the UI"""
        if data:
            marker_cluster = MapGenerator.add_marker_cluster(map_object)
            for _, row in data["merged_data"].iterrows():
                st.subheader(f"Postal Code: {row['PLZ']}")
                st.subheader(f"Available Stations: {row['Number']}")
                MapGenerator.add_marker(
                    map_object,
                    location=[float(row['Breitengrad']), float(row['Längengrad'])],
                    popup=f"PIN: {row['PLZ']}, Number: {row['Number']}",
                    icon_color='green'
                )

            for _, row in data["filtered_dframe2"].iterrows():
                MapGenerator.add_geojson_overlay(map_object, row['geometry'], row['PLZ'])

            folium_static(map_object, width=800, height=600)
        else:
            st.write("No charging stations found for this postal code.")


class ChargingStationApp:
    """Main application to search for charging stations"""

    def charging_station_search_by_postal_code(self, dframe1, dframe2):
        self.search_handler = PostalCodeSearch(dframe1, dframe2)

    def run(self) -> None:
        """Run the application"""
        map_center = [52.52, 13.40]  # Berlin center
        map_object = MapGenerator.create_base_map(map_center, 10)
        postal_code = UIHandler.render_sidebar()

        if postal_code:
            try:
                postal_code = int(postal_code)
                data = self.search_handler.filter_data_by_postal_code(postal_code)
                UIHandler.render_results(map_object, data)
            except ValueError:
                st.write("Please enter a valid postal code.")
        else:
            st.write("Enter a postal code and click 'Search' to find charging stations.")



class SearchService:
    def __init__(self, df_lstat):
        self.df_lstat = df_lstat
        # Configure logging
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    def search_by_postal_code(self, postal_code):
        """
        Searches the dataframe for stations by a given postal code.
        
        :param postal_code: The postal code to search for (string, int, or float).
        :return: A list of station dictionaries with name, status, and location.
        """
        try:
            # Validate the postal code
            if postal_code is None or not str(postal_code).strip().replace('.', '', 1).isdigit():
                logging.warning(f"Invalid postal code provided: {postal_code}")
                return []

            # Convert postal code to an integer for comparison
            postal_code = int(float(postal_code))
            logging.info(f"Searching for postal code: {postal_code}")
            
            # Normalize the postal codes in the dataframe
            self.df_lstat["Postleitzahl"] = self.df_lstat["Postleitzahl"].fillna(0).astype(float).astype(int)
            logging.info(f"Unique postal codes in the dataset: {self.df_lstat['Postleitzahl'].unique()}")

            # Filter the dataframe for the given postal code
            filtered_df = self.df_lstat[self.df_lstat["Postleitzahl"] == postal_code]
            logging.info(f"Filtered dataframe:\n{filtered_df}")

            # Prepare the list of stations
            stations = []
            for _, row in filtered_df.iterrows():
                try:
                    lat = float(str(row["Breitengrad"]).replace(',', '.'))
                    lon = float(str(row["Längengrad"]).replace(',', '.'))
                    stations.append({
                        "name": row["Anzeigename (Karte)"],
                        "status": "Available",  # Assuming default status as "Available"
                        "location": (lat, lon),
                    })
                except ValueError as e:
                    logging.error(f"Error parsing location for row: {row}\n{e}")

            return stations

        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            return []
