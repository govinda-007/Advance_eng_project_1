import folium
import streamlit as st
from folium.plugins import HeatMap, MarkerCluster
from streamlit_folium import folium_static
from shared.application import HelperTools as ht
import pandas as pd
from branca.colormap import LinearColormap
from streamlit_folium import st_folium
from charging.application.services.Search import SearchService
from charging.application.services import Search, Visualize, Suggestion
from charging.application.services.Suggestion import SuggestionManager, SuggestionUI, Suggestion
from charging.application.services.Visualize import Visualize
from charging.application.services.Postal_search import Search

class Application:
    """Main application class to coordinate all services"""

    def __init__(self, l_stat, dframe1, dframe2):
        self.l_stat = l_stat
        self.dframe1 = dframe1.copy()
        self.dframe2 = dframe2.copy()
        self.search_service = Search()
        self.visualize_service = Visualize()
        self.suggestion_service = Suggestion(SuggestionManager(),SuggestionUI())

    def run(self):
        """Run the Streamlit application"""
        st.title("Heatmaps: Electric Charging Stations and Residents")

        # Show heatmap layer selection
        layer_selection = self._show_layer_selection()
        self.visualize_service.render_map(self.dframe1, self.dframe2, layer_selection)

        # Handle menu options
        self._handle_menu()

    def _show_layer_selection(self):
        """Display layer selection radio buttons"""
        return st.radio("Select Layer", ("Residents", "Charging_Stations"))

    def _handle_menu(self):
        """Display sidebar menu and call the appropriate service"""
        #st.title("Charging Station Finder & Suggestions")
        menu = ["Search Charging Stations", "Suggest a New Location", "Vote on Suggestions"]
        choice = st.sidebar.selectbox("Menu", menu)

        if choice == "Search Charging Stations":
            self.search_service.search_by_postal_code(self.l_stat)
        elif choice == "Suggest a New Location":
            self.suggestion_service.display_suggestions_page()
        elif choice == "Vote on Suggestions":
            self.suggestion_service.display_voting_page()

# ---------------------------------------------------------------------------

# Entry point for the application
@ht.timer
def make_streamlit_electric_Charging_resid(dfr1, dfr2):
    """Main function to start the Streamlit application"""
    app = Application(dfr1, dfr2)
    app.run()
