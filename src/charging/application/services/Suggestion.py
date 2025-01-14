import streamlit as st
import pandas as pd

# Initialize a DataFrame to store suggestions (can be replaced with a database)
def init_suggestions():
    if "suggestions" not in st.session_state:
        st.session_state["suggestions"] = pd.DataFrame(columns=["Postal Code", "Location Name", "Latitude", "Longitude", "Description"])

def add_suggestion(postal_code, location_name, latitude, longitude, description):
    new_suggestion = pd.DataFrame({
        "Postal Code": [postal_code],
        "Location Name": [location_name],
        "Latitude": [latitude],
        "Longitude": [longitude],
        "Description": [description],
    })
    st.session_state["suggestions"] = pd.concat([st.session_state["suggestions"], new_suggestion], ignore_index=True)

def suggestions_page():
    """Page to handle user suggestions"""
    init_suggestions()

    st.sidebar.markdown("### Suggest a New Location")
    
    # Adding unique keys to each input element
    postal_code = st.sidebar.text_input("Enter Postal Code (PLZ)", key="postal_code_input")
    location_name = st.sidebar.text_input("Enter Location Name", key="location_name_input")
    latitude = st.sidebar.text_input("Enter Latitude", key="latitude_input")
    longitude = st.sidebar.text_input("Enter Longitude", key="longitude_input")
    description = st.sidebar.text_area("Enter a Description of the Location", key="description_input")
    suggest_button = st.sidebar.button("Submit Suggestion", key="submit_button")

    if suggest_button:
        if postal_code and location_name and latitude and longitude and description:
            try:
                latitude = float(latitude)
                longitude = float(longitude)
                add_suggestion(postal_code, location_name, latitude, longitude, description)
                st.success("Suggestion added successfully!")
            except ValueError:
                st.error("Please enter valid numerical values for latitude and longitude.")
        else:
            st.error("All fields are required.")

    st.markdown("### User Suggestions")
    suggestions_df = st.session_state["suggestions"]
    if not suggestions_df.empty:
        st.write(suggestions_df)
    else:
        st.write("No suggestions available yet.")



