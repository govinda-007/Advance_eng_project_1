import pytest
import pandas as pd
import streamlit as st
from unittest.mock import patch
from charging.application.services.Suggestion import SuggestionManager, SuggestionUI,Suggestion


@pytest.fixture
def setup_suggestion_manager():
    """Fixture to initialize SuggestionManager and clear session state."""
    st.session_state.clear()
    manager = SuggestionManager()
    manager.initialize()
    return manager

@pytest.fixture
def setup_suggestion_ui():
    """Fixture to create SuggestionUI instance."""
    return SuggestionUI()

@pytest.fixture
def setup_suggestion(setup_suggestion_manager, setup_suggestion_ui):
    """Fixture to create Suggestion instance."""
    return Suggestion(setup_suggestion_manager, setup_suggestion_ui)

def test_initialize_suggestions(setup_suggestion_manager):
    """Test if session state initializes correctly."""
    assert "suggestions" in st.session_state
    assert isinstance(st.session_state["suggestions"], pd.DataFrame)
    assert st.session_state["suggestions"].empty

def test_add_valid_suggestion(setup_suggestion_manager):
    """Test adding a valid suggestion."""
    setup_suggestion_manager.add_suggestion("10115", "Test Location", 52.52, 13.40, "A great place!")
    
    suggestions = setup_suggestion_manager.get_suggestions()
    
    assert not suggestions.empty
    assert suggestions.iloc[0]["Postal Code"] == "10115"
    assert suggestions.iloc[0]["Location Name"] == "Test Location"
    assert suggestions.iloc[0]["Latitude"] == 52.52
    assert suggestions.iloc[0]["Longitude"] == 13.40
    assert suggestions.iloc[0]["Description"] == "A great place!"

def test_add_duplicate_suggestion(setup_suggestion_manager):
    """Test preventing duplicate suggestions."""
    setup_suggestion_manager.add_suggestion("10115", "Test Location", 52.52, 13.40, "First entry")
    setup_suggestion_manager.add_suggestion("10115", "Test Location", 52.52, 13.40, "Duplicate entry")

    suggestions = setup_suggestion_manager.get_suggestions()

    assert len(suggestions) == 1  # Should still be only one entry

def test_get_suggestions_empty(setup_suggestion_manager):
    """Test retrieving suggestions when none exist."""
    suggestions = setup_suggestion_manager.get_suggestions()
    assert suggestions.empty

def test_get_suggestions_non_empty(setup_suggestion_manager):
    """Test retrieving suggestions after adding entries."""
    setup_suggestion_manager.add_suggestion("10117", "Another Place", 52.53, 13.41, "Nice location")
    
    suggestions = setup_suggestion_manager.get_suggestions()
    
    assert not suggestions.empty
    assert len(suggestions) == 1

def test_voting_functionality(setup_suggestion):
    """Test the upvote and downvote functionality."""
    setup_suggestion.suggestion_manager.add_suggestion("10118", "Vote Test", 52.54, 13.42, "Good spot")
    
    # Ensure Votes column exists
    st.session_state["suggestions"]["Votes"] = 0

    suggestions = setup_suggestion.suggestion_manager.get_suggestions()
    assert "Votes" in suggestions.columns
    assert suggestions.iloc[0]["Votes"] == 0

    # Simulate upvote
    setup_suggestion._cast_vote(0, "up")
    assert suggestions.iloc[0]["Votes"] == 1

    # Simulate downvote
    setup_suggestion._cast_vote(0, "down")
    assert suggestions.iloc[0]["Votes"] == 0  # Should not go below 0

def test_get_top_suggestions(setup_suggestion):
    """Test retrieving the top suggestions based on votes."""
    setup_suggestion.suggestion_manager.add_suggestion("10119", "Best Spot", 52.55, 13.43, "Amazing")
    setup_suggestion.suggestion_manager.add_suggestion("10120", "Cool Place", 52.56, 13.44, "Nice one")
    
    st.session_state["suggestions"]["Votes"] = [5, 3]  # Assign votes

    top_suggestions = setup_suggestion.get_top_suggestions(st.session_state["suggestions"], n=2)
    
    assert len(top_suggestions) == 2
    assert top_suggestions.iloc[0]["Votes"] >= top_suggestions.iloc[1]["Votes"]
