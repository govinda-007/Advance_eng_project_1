import pytest
import pandas as pd
import streamlit as st
from unittest.mock import patch
from charging.application.services.Suggestion import SuggestionManager, SuggestionUI

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
