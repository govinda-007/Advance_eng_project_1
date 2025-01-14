from shared.application import HelperTools     as ht
from charging.application.services import Search
from charging.application.services import Visualize
from charging.application.services import Voiting
from charging.application.services import Suggestion

import folium
# from folium.plugins import HeatMap
import streamlit as st
from streamlit_folium import folium_static
from branca.colormap import LinearColormap


# -----------------------------------------------------------------------------
@ht.timer
def make_streamlit_electric_Charging_resid(dfr1, dfr2):
    """Makes Streamlit App with Heatmap of Electric Charging Stations and Residents"""
    
    dframe1 = dfr1.copy()
    dframe2 = dfr2.copy()


    # Streamlit app
    st.title('Heatmaps: Electric Charging Stations and Residents')

    Search.charging_station_search_by_postal_code(dframe1, dframe2)
    # Create a radio button for layer selection
    # layer_selection = st.radio("Select Layer", ("Number of Residents per PLZ (Postal code)", "Number of Charging Stations per PLZ (Postal code)"))

    layer_selection = st.radio("Select Layer", ("Residents", "Charging_Stations"))

    Visualize.MapVisualize(dframe1, dframe2, layer_selection)

    st.title("Charging Station Finder & Suggestions")

    menu = ["Search Charging Stations", "Suggest a New Location"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Search Charging Stations":

        Search.charging_station_search_by_postal_code(dframe1, dframe2)
    elif choice == "Suggest a New Location":
        Suggestion.suggestions_page()
    elif choice == "Vote on Suggestions":
        Suggestion.voting_page()
