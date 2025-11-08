# components/tool_listings.py
import streamlit as st
from database.db_functions import add_data, get_data
import pandas as pd
from ai.ai_matcher import get_recommendations  # ✅ Gemini AI integration


def render_tool_listing(farmer_name):
    """Renders the form to add a new tool or machine listing with AI suggestions."""
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Add a Farm Tool for Rent")

    profile = st.session_state.get("farmer_profile", {})
    location_value = profile.get("location", "") if profile else ""
    contact_value = profile.get("contact", "") if profile else ""

    with st.form("tool_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            name = st.text_input("Your Name", value=farmer_name, key="tool_name_input")
            location = st.text_input("Your Location (Village)", value=location_value, key="tool_loc_input")
        with col2:
            tool_name = st.selectbox(
                "Tool Type",
                ["Tractor", "Plow", "Seeder", "Sprayer", "Harvester", "Other"],
                key="tool_type_select"
            )
            rent_rate = st.number_input("Rent Rate (per day)", min_value=0.0, format="%.2f", key="tool_rate_input")
        with col3:
            contact = st.text_input("Contact Number", value=contact_value, key="tool_contact_input")
            notes = st.text_area("Additional Notes (e.g., condition, availability)", height=80)
        
        submitted = st.form_submit_button("Add Tool Listing")

        if submitted:
            if name and location and tool_name and rent_rate > 0 and contact:
                tool_data = (name, location, tool_name, rent_rate, contact, notes)
                add_data("tools", tool_data)
                st.session_state.tools = get_data("tools")

                recs = get_recommendations({
                    "type": "tool",
                    "farmer": name,
                    "location": location,
                    "item": tool_name,
                    "notes": notes
                })
                st.info(f"Smart Suggestion: {recs}")

                st.success(f"Tool '{tool_name}' added successfully by {name}!")
            else:
                st.error("Please fill in all required fields.")

    st.markdown('</div>', unsafe_allow_html=True)


def render_tool_management(tools_df, farmer_name):
    """Renders the full tool management view with filtering and editable tables."""
    st.subheader("All Tool Listings")

    if not tools_df.empty:
        tools_without_rowid = tools_df.drop(columns=['rowid'])
        tool_locations = ["All"] + sorted(tools_without_rowid["Location"].unique().tolist())
        tool_types = ["All"] + sorted(tools_without_rowid["Tool"].unique().tolist())

        filter_cols = st.columns(3)
        selected_tool_loc = filter_cols[0].selectbox("Filter by Location", tool_locations, key="tool_loc_filter")
        selected_tool_type = filter_cols[1].selectbox("Filter by Tool Type", tool_types, key="tool_type_filter")

        filtered_tools = tools_without_rowid.copy()
        if selected_tool_loc != "All":
            filtered_tools = filtered_tools[filtered_tools["Location"] == selected_tool_loc]
        if selected_tool_type != "All":
            filtered_tools = filtered_tools[filtered_tools["Tool"] == selected_tool_type]

        st.dataframe(filtered_tools, use_container_width=True)
    else:
        st.info("No tools listed yet.")

    st.markdown('<hr>', unsafe_allow_html=True)
    if farmer_name:
        st.subheader(f"Your Tool Listings (Editable by {farmer_name})")
        editable_tools = tools_df[tools_df["Farmer"] == farmer_name]

        if not editable_tools.empty:
            editable_for_display = editable_tools.drop(columns=['rowid'])

            updated_tools_df = st.data_editor(
                editable_for_display,
                key="tool_editor",
                use_container_width=True,
                num_rows="dynamic"
            )
            st.session_state.tools.loc[updated_tools_df.index, updated_tools_df.columns] = updated_tools_df.values
        else:
            st.info("You have no tool listings yet.")
    else:
        st.warning("Please log in to view and manage your listings.")
