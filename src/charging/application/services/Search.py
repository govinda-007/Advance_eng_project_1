import folium
from folium.plugins import MarkerCluster
# from folium.plugins import HeatMap
import streamlit as st
from streamlit_folium import folium_static
from branca.colormap import LinearColormap


def charging_station_search_by_postal_code(dframe1, dframe2):
    """Search for charging stations by postal code and display on map"""
    st.sidebar.markdown("### Search Charging Stations by Postal Code")
    postal_code = st.sidebar.text_input("Enter Postal Code (PLZ)", "")
    search_button = st.sidebar.button("Search")

    map_center = [52.52, 13.40]  # Berlin center
    m = folium.Map(location=map_center, zoom_start=10)

    if search_button and postal_code:
        try:
            postal_code = int(postal_code)

            # Filter data from dframe1 and dframe2
            filtered_dframe1 = dframe1[dframe1['PLZ'] == postal_code]
            filtered_dframe2 = dframe2[dframe2['PLZ'] == postal_code]

            if not filtered_dframe1.empty and not filtered_dframe2.empty:
                # Merge data to include coordinates and numbers
                merged_data = filtered_dframe2.merge(
                    filtered_dframe1[['PLZ', 'Number']],
                    on='PLZ',
                    how='left'
                )

                # Highlight the postal code area with a yellow overlay
                for _, row in filtered_dframe2.iterrows():
                    
                    folium.GeoJson(
                        data=row['geometry'],
                        style_function=lambda x: {
                            'fillColor': 'yellow',
                            'color': 'black',
                            'weight': 2,
                            'fillOpacity': 0.5
                        },
                        tooltip=f"PLZ: {row['PLZ']}"
                    ).add_to(m)

                # Add markers to map
                marker_cluster = MarkerCluster().add_to(m)
                for _, row in merged_data.iterrows():
                    st.subheader(f"Pincode : {row['PLZ']} ")
                    st.subheader(f"Available : {row['Number']}")
                    folium.Marker(
                        location=[float(row['Breitengrad']), float(row['Längengrad'])],
                        popup=f"PIN: {row['PLZ']}, Number: {row['Number']}",
                        icon=folium.Icon(color='green')
                    ).add_to(marker_cluster)

                folium_static(m, width=800, height=600)
            else:
                st.write("No charging stations found for this postal code.")
        except ValueError:
            st.write("Please enter a valid postal code.")
    else:
        st.write("Enter a postal code and click 'Search' to find charging stations.")