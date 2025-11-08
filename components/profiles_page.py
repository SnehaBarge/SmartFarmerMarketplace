# components/profiles_page.py
import streamlit as st
from database.db_functions import add_data, get_data

def render_profiles_page():
    """Renders the page to manage farmer profiles."""
    st.subheader("Add New Farmer Profile")

    with st.form("new_farmer_form"):
        name = st.text_input("Farmer's Name")
        location = st.text_input("Location (Village)")
        farm_size = st.number_input("Farm Size", min_value=0.0, format="%.2f")
        farm_unit = st.selectbox("Farm Size Unit", ["Acres", "Hectares"])
        contact = st.text_input("Contact Number")
        
        submitted = st.form_submit_button("Add Farmer")
        
        if submitted:
            if name and location and farm_size > 0 and contact:
                farmer_data = (name, location, farm_size, farm_unit, contact)
                add_data("farmers", farmer_data)
                st.success(f"Farmer '{name}' added successfully!")
            else:
                st.error("Please fill in all fields.")

    st.markdown("<hr>", unsafe_allow_html=True)

    st.subheader("All Farmer Profiles")
    farmers_df = get_data("farmers")
    st.dataframe(farmers_df)
