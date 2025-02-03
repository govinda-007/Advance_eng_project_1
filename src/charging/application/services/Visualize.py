import folium
from folium.plugins import MarkerCluster
import streamlit as st
from streamlit_folium import folium_static
from branca.colormap import LinearColormap
from typing import Any, Dict, List
import pandas as pd


class Visualize:
    """Handles map visualization"""
    def __init__(self):
        pass
     
    def render_map(self, dframe1, dframe2, layer_selection):
        if layer_selection == "Residents":
            self._render_residents_layer(dframe2)
        elif layer_selection == "Charging_Stations":
            self._render_charging_stations_layer(dframe1)

    def _render_residents_layer(self, dframe2):
        # Create a Folium map
        m = folium.Map(location=[52.52, 13.40], zoom_start=10)
        color_map = LinearColormap(colors=['yellow', 'red'], vmin=dframe2['Einwohner'].min(), vmax=dframe2['Einwohner'].max())

        # Add polygons to the map for Residents
        for idx, row in dframe2.iterrows():
            folium.GeoJson(
                row['geometry'],
                style_function=lambda x, color=color_map(row['Einwohner']): {
                    'fillColor': color,
                    'color': 'black',
                    'weight': 1,
                    'fillOpacity': 0.7
                },
                tooltip=f"PLZ: {row['PLZ']}, Einwohner: {row['Einwohner']}"
            ).add_to(m)
        
        # Display the dataframe for Residents
        # st.subheader('Residents Data')
        # st.dataframe(gdf_residents2)
        # Add color map to the map
        color_map.add_to(m)
    
        folium_static(m, width=800, height=600)


    def _render_charging_stations_layer(self, dframe1):

        m = folium.Map(location=[52.52, 13.40], zoom_start=10)

        color_map = LinearColormap(colors=['yellow', 'red'], vmin=dframe1['Number'].min(), vmax=dframe1['Number'].max())

    # Add polygons to the map for Numbers
        for idx, row in dframe1.iterrows():
            folium.GeoJson(
                row['geometry'],
                style_function=lambda x, color=color_map(row['Number']): {
                    'fillColor': color,
                    'color': 'black',
                    'weight': 1,
                    'fillOpacity': 0.7
                },
                tooltip=f"PLZ: {row['PLZ']}, Number: {row['Number']}"
            ).add_to(m)

        # Display the dataframe for Numbers
        # st.subheader('Numbers Data')
        # st.dataframe(gdf_lstat3)

    # Add color map to the map
        color_map.add_to(m)
        folium_static(m, width=800, height=600)
        