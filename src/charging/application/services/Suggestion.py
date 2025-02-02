'''import streamlit as st
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
    def add_suggestion(postal_code: str, location_name: str, latitude: float, longitude: float, description: str) -> None:
        """Add a new suggestion to the storage."""
        new_suggestion = pd.DataFrame({
            "Postal Code": [postal_code],
            "Location Name": [location_name],
            "Latitude": [latitude],
            "Longitude": [longitude],
            "Description": [description],
        })
        st.session_state["suggestions"] = pd.concat([st.session_state["suggestions"], new_suggestion], ignore_index=True)

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


class SuggestionApp:
    """Main application class to handle suggestions."""

    def __init__(self, suggestion_manager: SuggestionManager, ui: SuggestionUI):
        self.suggestion_manager = suggestion_manager
        self.ui = ui

    def run(self):
        """Run the suggestion application."""
        self.suggestion_manager.initialize()

        # Add a sidebar dropdown to select the action
        st.sidebar.title("Navigation")
        selected_option = st.sidebar.selectbox(
            "Choose an option",
            ["View Suggestions", "Suggest a New Location", "Vote on Suggestions"]
        )

        if selected_option == "Suggest a New Location":
            # Render the input form and handle submission
            postal_code, location_name, latitude, longitude, description, submit_button = self.ui.render_input_form()

            if submit_button:
                # Validate and add the suggestion
                if postal_code and location_name and latitude and longitude and description:
                    try:
                        latitude = float(latitude)
                        longitude = float(longitude)
                        self.suggestion_manager.add_suggestion(
                            postal_code, location_name, latitude, longitude, description
                        )
                        self.ui.show_success_message("Suggestion added successfully!")
                    except ValueError:
                        self.ui.show_error_message("Please enter valid numerical values for latitude and longitude.")
                else:
                    self.ui.show_error_message("All fields are required.")

        elif selected_option == "View Suggestions":
            # Render the suggestions list
            suggestions_df = self.suggestion_manager.get_suggestions()
            self.ui.render_suggestions_list(suggestions_df)

# Dependency Injection in Action
if __name__ == "__main__":
    app1 = SuggestionApp(SuggestionManager(), SuggestionUI())
    app1.run()'''

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


class SuggestionApp:
    """Main application class to handle suggestions."""

    def __init__(self, suggestion_manager: SuggestionManager, ui: SuggestionUI):
        self.suggestion_manager = suggestion_manager
        self.ui = ui

    def run(self):
        """Run the suggestion application."""
        self.suggestion_manager.initialize()

        # Add a sidebar dropdown to select the action
        st.sidebar.title("Navigation")
        selected_option = st.sidebar.selectbox(
            "Choose an option",
            ["View Suggestions", "Suggest a New Location", "Vote on Suggestions"]
        )

        if selected_option == "Suggest a New Location":
            # Render the input form and handle submission
            postal_code, location_name, latitude, longitude, description, submit_button = self.ui.render_input_form()

            if submit_button:
                # Validate and add the suggestion
                if postal_code and location_name and latitude and longitude and description:
                    try:
                        latitude = float(latitude)
                        longitude = float(longitude)
                        self.suggestion_manager.add_suggestion(
                            postal_code, location_name, latitude, longitude, description
                        )
                        self.ui.show_success_message("Suggestion added successfully!")
                    except ValueError:
                        self.ui.show_error_message("Please enter valid numerical values for latitude and longitude.")
                else:
                    self.ui.show_error_message("All fields are required.")

        elif selected_option == "View Suggestions":
            # Render the suggestions list
            suggestions_df = self.suggestion_manager.get_suggestions()
            self.ui.render_suggestions_list(suggestions_df)





# Dependency Injection in Action
# if __name__ == "__main__":
#     app1 = SuggestionApp(SuggestionManager(), SuggestionUI())
#     app1.run()
