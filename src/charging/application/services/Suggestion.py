import streamlit as st
import pandas as pd


# Single Responsibility Principle (SRP)
# Separate the responsibilities into different classes or functions.

class SuggestionManager:
    """Handles storage and manipulation of suggestions."""

    @staticmethod
    def initialize():
        """Initialize the suggestions DataFrame."""
        if "suggestions" not in st.session_state:
            st.session_state["suggestions"] = pd.DataFrame(
                columns=["Postal Code", "Location Name", "Latitude", "Longitude", "Description"]
            )

    @staticmethod
    def add_suggestion(postal_code: str, location_name: str, latitude: float, longitude: float,
                       description: str) -> None:
        """Add a new suggestion to the storage."""

        if (
                postal_code.isnumeric() and
                len(location_name) > 0 and
                isinstance(latitude, float) and isinstance(longitude,float)
                and len(description) > 0
        ):
            # Check for duplicates based on Postal Code and Location Name
            existing_suggestions = st.session_state["suggestions"]
            duplicate_check = existing_suggestions[
                (existing_suggestions["Postal Code"] == postal_code) &
                (existing_suggestions["Location Name"] == location_name)
                ]

            if duplicate_check.empty:
                # If no duplicate is found, add the new suggestion
                new_suggestion = pd.DataFrame({
                    "Postal Code": [postal_code],
                    "Location Name": [location_name],
                    "Latitude": [latitude],
                    "Longitude": [longitude],
                    "Description": [description],
                })
                st.session_state["suggestions"] = pd.concat([st.session_state["suggestions"], new_suggestion],
                                                            ignore_index=True)


    @staticmethod
    def get_suggestions() -> pd.DataFrame:
        """Retrieve the suggestions DataFrame."""
        return st.session_state.get("suggestions", pd.DataFrame())


# Open/Closed Principle (OCP)
# UI components can be extended with new functionality without modifying existing code.

class SuggestionUI:
    """Handles the user interface for suggestions."""

    @staticmethod
    def render_input_form():
        """Render the form for user input."""
        st.markdown("### Suggest a New Location")
        with st.form(key="suggestion_form"):
            postal_code = st.text_input("Enter Postal Code (PLZ)")
            location_name = st.text_input("Enter Location Name")
            latitude = st.text_input("Enter Latitude")
            longitude = st.text_input("Enter Longitude")
            description = st.text_area("Enter a Description of the Location")
            submit_button = st.form_submit_button("Submit Suggestion")
        return postal_code, location_name, latitude, longitude, description, submit_button

    @staticmethod
    def render_suggestions_list(suggestions_df: pd.DataFrame):
        """Render the list of user suggestions."""
        st.markdown("### User Suggestions")
        if not suggestions_df.empty:
            st.dataframe(suggestions_df)
        else:
            st.write("No suggestions available yet.")

    @staticmethod
    def show_success_message(message: str):
        """Display a success message."""
        st.success(message)

    @staticmethod
    def show_error_message(message: str):
        """Display an error message."""
        st.error(message)



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
