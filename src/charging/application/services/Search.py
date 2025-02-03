import folium
from folium.plugins import MarkerCluster
import streamlit as st
import pandas as pd
from streamlit_folium import folium_static
from streamlit_folium import st_folium
from branca.colormap import LinearColormap
from typing import Any, Dict, List
import logging

# SOLID Refactor

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
     

