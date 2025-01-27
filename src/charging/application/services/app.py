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
from charging.application.services.Suggestion import SuggestionManager,SuggestionUI


class Application:
    """Main application class to coordinate all services"""

    def __init__(self, dframe1, dframe2):
        self.dframe1 = dframe1.copy()
        self.dframe2 = dframe2.copy()
        self.search_service = Search()
        self.visualize_service = Visualize()
        self.suggestion_service = Suggestion(SuggestionManager(), SuggestionUI())

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
            self.search_service.search_by_postal_code(self.dframe2)
        elif choice == "Suggest a New Location":
            self.suggestion_service.display_suggestions_page()
        elif choice == "Vote on Suggestions":
            self.suggestion_service.display_voting_page()


# ---------------------------------------------------------------------------
class Search:
    """Handles searching of charging stations"""

    def search_by_postal_code(self, dframe2):
        st.sidebar.markdown("### Search Charging Stations by Postal Code")
        postal_code = st.sidebar.text_input("Enter Postal Code (PLZ)", "")
        search_button = st.sidebar.button("Search")
        search_service = SearchService(dframe2)

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
                #      popup=f"{station['name']} ({station['status']})",
                        popup=f"Is ready for you)",
                        # popup=f"{station['name']} Is ready for you)",
                        # icon=folium.Icon(color="green" if station["status"] == "available" else "red"),
                    ).add_to(m)
                st_folium(m, width=700, height=500)
            else:
                st.warning("No charging stations found for this postal code.")

# ---------------------------------------------------------------------------
class Visualize:
    """Handles map visualization"""

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
        


# ---------------------------------------------------------------------------
class Suggestion:
    """Handles suggestion-related functionality"""

    def __init__(self, suggestion_manager: SuggestionManager, ui: SuggestionUI):
        self.suggestion_manager = suggestion_manager
        self.ui = ui
    
    def get_top_suggestions(self, suggestions_df, n: int = 3):
        """Retrieve the top N suggestions based on votes."""
        return suggestions_df.sort_values(by="Votes", ascending=False).head(n)
    
    def _cast_vote(self, index: int, vote: str):
        """Cast an upvote or downvote on a suggestion."""
        suggestions_df = st.session_state["suggestions"]
        if vote == "up":
            suggestions_df.at[index, "Votes"] += 1
        elif vote == "down":
            current_votes = suggestions_df.at[index, "Votes"]
            suggestions_df.at[index, "Votes"] = max(0, current_votes - 1)
        st.session_state["suggestions"] = suggestions_df


    def display_suggestions_page(self):
        """Display the suggestion submission form"""
        self.suggestion_manager.initialize()
        postal_code, location_name, lat, longitude, description, submit_button = self.ui.render_input_form()

        if submit_button:
            # Validate and add the suggestion
            if postal_code and location_name and lat and longitude and description:
                try:
                    lat = float(lat)
                    longitude = float(longitude)
                    self.suggestion_manager.add_suggestion(postal_code, location_name, lat, longitude, description)
                    self.ui.show_success_message("Suggestion added successfully!")
                except ValueError:
                    self.ui.show_error_message("Please enter valid numerical values for lat and longitude.")
            else:
                self.ui.show_error_message("All fields are required.")

        # Display the list of suggestions after submission
        suggestions_df = self.suggestion_manager.get_suggestions()
        self.ui.render_suggestions_list(suggestions_df)

    def display_voting_page(self):
        """Display voting options for suggestions."""
        self.suggestion_manager.initialize()
        suggestions_df = self.suggestion_manager.get_suggestions()

        if suggestions_df.empty:
            st.write("No suggestions available to vote on.")
            return

        # Ensure Votes column exists
        if "Votes" not in suggestions_df.columns:
            suggestions_df["Votes"] = 0
            st.session_state["suggestions"] = suggestions_df

        # Display suggestions with voting buttons
        st.markdown("### Vote on User Suggestions")
        for index, row in suggestions_df.iterrows():
            st.markdown(f"#### {row['Location Name']} (Postal Code: {row['Postal Code']})")
            st.write(f"Description: {row['Description']}")
            

            col1, col2 = st.columns(2)
            with col1:
                if st.button("👍 Thumbs Up", key=f"upvote_{index}"):
                    self._cast_vote(index, "up")
            with col2:
                if st.button("👎 Thumbs Down", key=f"downvote_{index}"):
                    self._cast_vote(index, "down")


        # Show top suggestions
        top_suggestions = self.get_top_suggestions(suggestions_df)
        
        st.markdown("### Top 3 Suggestions")
        if not top_suggestions.empty:
            for _, row in top_suggestions.iterrows():
                st.markdown(
                    # st.write(f"Votes: {row['Votes']}"),
                    f"- **{row['Location Name']}** (Postal Code: {row['Postal Code']}) - Votes: {row['Votes']}"
                )
        else:
            st.write("No top suggestions available.")






# ---------------------------------------------------------------------------
# Entry point for the application
@ht.timer
def make_streamlit_electric_Charging_resid(dfr1, dfr2):
    """Main function to start the Streamlit application"""
    app = Application(dfr1, dfr2)
    app.run()
