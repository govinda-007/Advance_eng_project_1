import folium
from folium.plugins import MarkerCluster
import streamlit as st
import pandas as pd
from streamlit_folium import folium_static
from streamlit_folium import st_folium
from branca.colormap import LinearColormap
from typing import Any, Dict, List
import logging
from charging.application.services.Search import SearchService


class Search:
    """Handles searching of charging stations"""

    def search_by_postal_code(self, l_stat):
        

         
        # print("l_stat:", l_stat)
        st.sidebar.markdown("### Search Charging Stations by Postal Code")
        postal_code = st.sidebar.text_input("Enter Postal Code (PLZ)", "")
        search_button = st.sidebar.button("Search")
        search_service = SearchService(l_stat)
        print('searchService', search_service)

        if postal_code:
            st.write(f"Searching for postal code: {postal_code}")
            stations = search_service.search_by_postal_code(postal_code)
            print('stationData', stations)
            st.write(f"those are the stations in postal code :{postal_code}")
            st.write(pd.DataFrame(stations))
            print("station are as follow" )
            print(stations)
            # st.write("Debug - Stations Data:", stations)   # Debug output
            if stations:
                m = folium.Map(location=[52.5200, 13.4050], zoom_start=12)
                for station in stations:
                    folium.Marker(
                        location=station["location"],
                        # popup=f"{station['name']} ({station['status']})",
                        # popup=f"Is ready for you)",
                        popup=f"{station['name']} Is ready for you)",
                        # icon=folium.Icon(color="green" if station["status"] == "available" else "red"),
                    ).add_to(m)
                st_folium(m, width=700, height=500)
            else:
                st.warning("No charging stations found for this postal code.")
