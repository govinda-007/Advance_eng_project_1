import pytest
import pandas as pd
import streamlit as st
from unittest.mock import patch
from charging.application.services.Suggestion import SuggestionManager, SuggestionApp


@pytest.fixture
def setup_session_state():
    """Ensure a clean session state before each test."""
    st.session_state.clear()
    SuggestionManager.initialize()


def test_initialize_suggestions(setup_session_state):
    """Test that the suggestions DataFrame is initialized properly."""
    assert "suggestions" in st.session_state
    assert isinstance(st.session_state["suggestions"], pd.DataFrame)
    assert st.session_state["suggestions"].empty


def test_add_suggestion(setup_session_state):
    """Test adding a new suggestion and ensuring it is stored correctly."""
    SuggestionManager.add_suggestion("10115", "Berlin Mitte", 52.5200, 13.4050, "Popular tourist area.")
    suggestions_df = SuggestionManager.get_suggestions()
    assert len(suggestions_df) == 1
    assert suggestions_df.iloc[0]["Postal Code"] == "10115"
    assert suggestions_df.iloc[0]["Location Name"] == "Berlin Mitte"
    assert suggestions_df.iloc[0]["Latitude"] == 52.5200
    assert suggestions_df.iloc[0]["Longitude"] == 13.4050
    assert suggestions_df.iloc[0]["Description"] == "Popular tourist area."


def test_get_suggestions_empty(setup_session_state):
    """Test retrieving suggestions when there are no suggestions yet."""
    suggestions_df = SuggestionManager.get_suggestions()
    assert suggestions_df.empty


def test_get_suggestions_non_empty(setup_session_state):
    """Test retrieving suggestions when at least one suggestion exists."""
    SuggestionManager.add_suggestion("20095", "Hamburg", 53.5511, 9.9937, "Beautiful port city.")
    suggestions_df = SuggestionManager.get_suggestions()
    assert not suggestions_df.empty
    assert len(suggestions_df) == 1


def test_add_suggestion_invalid_postal_code(setup_session_state):
    """Test adding a suggestion with an invalid postal code."""
    SuggestionManager.add_suggestion("INVALID", "Invalid Location", 52.5200, 13.4050, "Description")
    suggestions_df = SuggestionManager.get_suggestions()
    assert len(suggestions_df) == 0  # Ensure it still gets added, or you can check for validation error


def test_add_suggestion_empty_location_name(setup_session_state):
    """Test adding a suggestion with an empty location name."""
    SuggestionManager.add_suggestion("10115", "", 52.5200, 13.4050, "Description")
    suggestions_df = SuggestionManager.get_suggestions()
    assert len(suggestions_df) == 0  # Ensure it still gets added, or you can check for validation error


def test_add_suggestion_empty_fields(setup_session_state):
    """Test adding a suggestion with empty fields."""
    SuggestionManager.add_suggestion("", "", "", "", "")
    suggestions_df = SuggestionManager.get_suggestions()
    assert len(suggestions_df) == 0  # Ensure no empty suggestions are added


def test_add_duplicate_suggestion(setup_session_state):
    """Test adding a duplicate suggestion."""
    SuggestionManager.add_suggestion("10115", "Berlin Mitte", 52.5200, 13.4050, "Popular tourist area.")
    SuggestionManager.add_suggestion("10115", "Berlin Mitte", 52.5200, 13.4050, "Popular tourist area.")
    suggestions_df = SuggestionManager.get_suggestions()
    assert len(suggestions_df) == 1  # Ensure no duplicates are added


def test_add_large_number_of_suggestions(setup_session_state):
    """Test adding a large number of suggestions."""
    for i in range(1000):
        SuggestionManager.add_suggestion(f"101{i}", f"Location {i}", 52.5200, 13.4050, f"Description {i}")
    suggestions_df = SuggestionManager.get_suggestions()
    assert len(suggestions_df) == 1000  # Ensure all suggestions are added correctly


def test_add_suggestion_invalid_latitude_longitude(setup_session_state):
    """Test adding a suggestion with invalid latitude and longitude."""
    SuggestionManager.add_suggestion("10115", "Berlin Mitte", "invalid_latitude", "invalid_longitude", "Description")
    suggestions_df = SuggestionManager.get_suggestions()
    assert len(suggestions_df) == 0  # Ensure the suggestion is not added due to invalid data types


def test_get_suggestions_when_empty(setup_session_state):
    """Test that the suggestions DataFrame is empty when there are no suggestions."""
    suggestions_df = SuggestionManager.get_suggestions()
    assert suggestions_df.empty  # Ensure it's empty


def test_add_suggestion_with_special_characters(setup_session_state):
    """Test adding a suggestion with special characters."""
    SuggestionManager.add_suggestion("10115", "Berlin Mitte @#$%", 52.5200, 13.4050, "Special character test!")
    suggestions_df = SuggestionManager.get_suggestions()
    assert len(suggestions_df) == 1  # Ensure the special characters are handled correctly


def test_session_state_persistence(setup_session_state):
    """Test that suggestions persist across function calls."""
    SuggestionManager.add_suggestion("10115", "Berlin Mitte", 52.5200, 13.4050, "Popular tourist area.")
    suggestions_df = SuggestionManager.get_suggestions()
    assert len(suggestions_df) == 1  # Ensure suggestion is present in the session state

    # Simulate reloading the page
    SuggestionManager.initialize()
    suggestions_df = SuggestionManager.get_suggestions()
    assert len(suggestions_df) == 1  # Ensure suggestion persists after initialization

import pytest
from unittest.mock import patch, MagicMock
import streamlit as st
from charging.application.services.Suggestion import SuggestionUI

def test_render_input_form_valid_input():
    # Mocking Streamlit's input and submit button behavior
    with patch("streamlit.text_input") as mock_text_input, \
         patch("streamlit.text_area") as mock_text_area, \
         patch("streamlit.form_submit_button") as mock_submit_button:

        # Simulating user inputs for different form fields
        mock_text_input.side_effect = [
            "12345",  # Postal Code
            "LOL",    # Location Name
            "123",    # Latitude
            "123",    # Longitude
        ]
        mock_text_area.return_value = "Test Description"
        mock_submit_button.return_value = True  # Simulating that the button is clicked

        # Call the render_input_form method
        postal_code, location_name, latitude, longitude, description, submit_button = SuggestionUI.render_input_form()

        # Assert that the mock values are returned correctly
        assert postal_code == "12345"
        assert location_name == "LOL"
        assert latitude == "123"
        assert longitude == "123"
        assert description == "Test Description"
        assert submit_button is True

def test_render_suggestions_list_with_data():
    # Prepare a non-empty DataFrame
    data = {
        "Postal Code": ["12345", "67890"],
        "Location Name": ["Test Location 1", "Test Location 2"],
        "Latitude": [40.7128, 34.0522],
        "Longitude": [-74.0060, -118.2437],
        "Description": ["Description 1", "Description 2"],
    }
    suggestions_df = pd.DataFrame(data)

    # Mocking Streamlit's functions
    with patch("streamlit.dataframe") as mock_data_frame, \
         patch("streamlit.write") as mock_write:

        # Call the render_suggestions_list method
        SuggestionUI.render_suggestions_list(suggestions_df)

        # Assert that st.dataframe was called with the correct DataFrame
        mock_data_frame.assert_called_once_with(suggestions_df)
        mock_write.assert_not_called()  # st.write should not be called



@patch("streamlit.success")
def test_show_success_message(mock_success):
    """Test success message rendering."""
    SuggestionUI.show_success_message("Test success message.")
    mock_success.assert_called_once_with("Test success message.")


@patch("streamlit.error")
def test_show_error_message(mock_error):
    """Test error message rendering."""
    SuggestionUI.show_error_message("Test error message.")
    mock_error.assert_called_once_with("Test error message.")


@patch("streamlit.error")
def test_show_error_message_on_empty_form(mock_error):
    """Test error message when the form is submitted with empty fields."""
    SuggestionUI.show_error_message("All fields are required.")
    mock_error.assert_called_once_with("All fields are required.")


@patch("streamlit.error")
def test_invalid_latitude_longitude_input(mock_error):
    """Test error handling for invalid latitude and longitude inputs."""
    SuggestionUI.show_error_message("Please enter valid numerical values for latitude and longitude.")
    mock_error.assert_called_once_with("Please enter valid numerical values for latitude and longitude.")


@pytest.fixture
def mock_suggestion_manager():
    return MagicMock(spec=SuggestionManager)

@pytest.fixture
def mock_ui():
    return MagicMock(spec=SuggestionUI)

@pytest.fixture
def app(mock_suggestion_manager, mock_ui):
    return SuggestionApp(mock_suggestion_manager, mock_ui)

def test_suggestion_app_initialization(mock_suggestion_manager, mock_ui):
    """Test if SuggestionApp initializes properly."""
    app = SuggestionApp(mock_suggestion_manager, mock_ui)
    assert app.suggestion_manager == mock_suggestion_manager
    assert app.ui == mock_ui


@patch("streamlit.sidebar.selectbox")
@patch("streamlit.sidebar.title")
def test_run_suggest_new_location(mock_sidebar_title, mock_sidebar_selectbox, app, mock_suggestion_manager, mock_ui):
    """Test 'Suggest a New Location' flow with valid input."""

    # Mock sidebar selection
    mock_sidebar_selectbox.return_value = "Suggest a New Location"

    # Mock form inputs
    mock_ui.render_input_form.return_value = ("12345", "Test Location", "40.7128", "-74.0060", "Test description", True)

    with patch("streamlit.success"), patch("streamlit.error"):
        app.run()

    # Ensure initialize is called
    mock_suggestion_manager.initialize.assert_called_once()

    # Ensure form is rendered
    mock_ui.render_input_form.assert_called_once()

    # Ensure add_suggestion is called with correct parameters
    mock_suggestion_manager.add_suggestion.assert_called_once_with("12345", "Test Location", 40.7128, -74.0060,
                                                                   "Test description")

    # Ensure success message is displayed
    mock_ui.show_success_message.assert_called_once_with("Suggestion added successfully!")


def test_run_suggest_new_location_invalid_coordinates(app, mock_suggestion_manager, mock_ui):
    """Test 'Suggest a New Location' flow with invalid latitude/longitude input."""

    with patch("streamlit.sidebar.selectbox", return_value="Suggest a New Location"), \
            patch("streamlit.sidebar.title"), \
            patch("streamlit.error") as mock_error:
        # Mock incorrect input where latitude and longitude are not convertible to float
        mock_ui.render_input_form.return_value = (
        "12345", "Test Location", "invalid_lat", "invalid_long", "Test description", True)

        app.run()

        # Ensure error message is displayed
        mock_ui.show_error_message.assert_called_once_with(
            "Please enter valid numerical values for latitude and longitude.")


def test_run_suggest_new_location_missing_fields(app, mock_suggestion_manager, mock_ui):
    """Test 'Suggest a New Location' with missing required fields."""

    with patch("streamlit.sidebar.selectbox", return_value="Suggest a New Location"), \
            patch("streamlit.sidebar.title"), \
            patch("streamlit.error") as mock_error:
        # Mock missing fields
        mock_ui.render_input_form.return_value = ("", "", "", "", "", True)

        app.run()

        # Ensure error message is displayed
        mock_ui.show_error_message.assert_called_once_with("All fields are required.")


@patch("streamlit.sidebar.selectbox")
@patch("streamlit.sidebar.title")
def test_run_view_suggestions(mock_sidebar_title, mock_sidebar_selectbox, app, mock_suggestion_manager, mock_ui):
    """Test 'View Suggestions' option."""

    mock_sidebar_selectbox.return_value = "View Suggestions"

    # Mock suggestion retrieval
    mock_suggestions_df = pd.DataFrame({
        "Postal Code": ["12345"],
        "Location Name": ["Test Location"],
        "Latitude": [40.7128],
        "Longitude": [-74.0060],
        "Description": ["Test description"]
    })
    mock_suggestion_manager.get_suggestions.return_value = mock_suggestions_df

    app.run()

    # Ensure suggestions are retrieved
    mock_suggestion_manager.get_suggestions.assert_called_once()

    # Ensure UI renders suggestions
    mock_ui.render_suggestions_list.assert_called_once_with(mock_suggestions_df)