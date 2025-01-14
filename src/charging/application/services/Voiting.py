import streamlit as st
import pandas as pd
from charging.application.services import Suggestion

# Initialize suggestions with votes if not already done
def init_votes():
    if "suggestions" not in st.session_state:
        st.session_state["suggestions"] = pd.DataFrame(columns=[
            "Postal Code", "Location Name", "Latitude", "Longitude", "Description", "Votes"
        ])
    elif "Votes" not in st.session_state["suggestions"].columns:
        st.session_state["suggestions"]["Votes"] = 0

def cast_vote(index, vote):
    """Cast a thumbs up or down vote on a suggestion"""
    if vote == "up":
        st.session_state["suggestions"].at[index, "Votes"] += 1
    elif vote == "down":
        st.session_state["suggestions"].at[index, "Votes"] -= 1

def voting_page():
    """Page to handle voting on suggestions"""
    init_votes()

    st.markdown("### Vote on Suggested Charging Locations")

    suggestions_df = st.session_state["suggestions"]
    if not suggestions_df.empty:
        # Display suggestions with voting options
        for index, row in suggestions_df.iterrows():
            st.markdown(f"#### {row['Location Name']} (Postal Code: {row['Postal Code']})")
            st.write(f"Description: {row['Description']}")
            st.write(f"Votes: {row['Votes']}")
            col1, col2 = st.columns(2)

            with col1:
                if st.button("👍 Thumbs Up", key=f"upvote_{index}"):
                    cast_vote(index, "up")

            with col2:
                if st.button("👎 Thumbs Down", key=f"downvote_{index}"):
                    cast_vote(index, "down")

        # Display top 3 suggestions based on votes
        st.markdown("### Top 3 Suggestions")
        top_suggestions = suggestions_df.sort_values(by="Votes", ascending=False).head(3)
        for _, row in top_suggestions.iterrows():
            st.markdown(f"- **{row['Location Name']}** (Postal Code: {row['Postal Code']}) - Votes: {row['Votes']}")

    else:
        st.write("No suggestions available to vote on.")
