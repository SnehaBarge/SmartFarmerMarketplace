import streamlit as st
import pandas as pd
from datetime import date
from dotenv import load_dotenv # <-- NEW: Used to load the .env file
import os

# Load environment variables from the .env file immediately
load_dotenv()

# ----------------------------------------
# --- 0. MODULE IMPORTS ---
# ----------------------------------------
from database.db_functions import init_db, get_data, add_data, get_farmer_profile
from components.home_page import render_home_page, render_db_check
from components.tool_listings import render_tool_listing, render_tool_management
from components.crop_listings import render_crop_listing, render_crop_management
from components.profiles_page import render_profiles_page

# ----------------------------------------
# --- CONFIGURATION AND SETUP ---
# ----------------------------------------

# 1. Database Initialization
if 'db_initialized' not in st.session_state:
    init_db()
    st.session_state.db_initialized = True

# 2. Page Config
st.set_page_config(page_title="Smart Farmer Marketplace", page_icon="favicon.ico", layout="wide")

# 3. Custom CSS for styling
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

    body { 
        font-family: 'Roboto', sans-serif;
        background-color: #f5f5f5;
    }
    h1,h2,h3 { 
        color:#2E8B57; 
        text-align:center; 
        font-weight:700; 
    }
    .stApp {
        background-color: #f5f5f5;
    }
    [data-testid="stSidebar"] { 
        background-color:#FFFFFF; 
        border-right:2px solid #E0E0E0; 
        padding-top:20px; 
    }
    
    /* Button Styling */
    .stButton>button { 
        background-color:#2E8B57; 
        color:white; 
        border-radius:8px; 
        padding:10px 20px; 
        font-weight:bold; 
        border:none; 
        box-shadow:0 2px 4px rgba(0,0,0,0.1); 
        width:100%; 
        transition: all 0.3s ease;
    }
    .stButton>button:hover { 
        background-color:#3CB371; 
        box-shadow:0 4px 8px rgba(0,0,0,0.2);
        transform: translateY(-2px);
    }
    
    /* Card Styling */
    .card { 
        background-color:#ffffff; 
        padding:30px; 
        margin-bottom:25px; 
        border-radius:15px; 
        box-shadow:0 8px 16px rgba(0,0,0,0.1); 
        border-left:7px solid #2E8B57; 
    }
    
    footer { 
        visibility:hidden; 
    }
    .stDataFrame, .stDataEditor { 
        border:1px solid #E0E0E0; 
        border-radius:10px; 
        padding:10px; 
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 4. Persistent Database Loading
st.session_state.tools = get_data("tools")
st.session_state.crops = get_data("crops")


# ----------------------------------------
# --- USER LOGIN ---
# ----------------------------------------
with st.sidebar.expander("User Login", expanded=True):
    login_as = st.radio("Login As", ["Farmer", "Admin"])

    if login_as == "Farmer":
        farmer_name = st.text_input("Enter your name", key="login_name").strip()
        if farmer_name:
            st.session_state.logged_in = True
            st.session_state.role = "Farmer"
            st.session_state.farmer_name = farmer_name
            st.session_state.farmer_profile = get_farmer_profile(farmer_name)
            st.success(f"Logged in as {farmer_name}")

    elif login_as == "Admin":
        password = st.text_input("Enter admin password", type="password", key="password_input")
        if password == "admin": # Hardcoded password for simplicity
            st.session_state.logged_in = True
            st.session_state.role = "Admin"
            st.session_state.farmer_name = "Admin"
            st.success("Logged in as Admin")
        elif password:
            st.error("Incorrect password")

# ----------------------------------------
# --- MAIN APPLICATION LOGIC ---
# ----------------------------------------
st.title("Smart Farmer Marketplace")

st.markdown("""
<div style='background-color:#E8F5E9;padding:12px;border-radius:10px;text-align:center;margin-bottom:20px;border: 1px dashed #3CB371;'>
    <h4>Empowering Farmers, Connecting Communities</h4>
</div>
""", unsafe_allow_html=True)

menu_options = ["Home", "New Listing", "View Listings"]
if st.session_state.get("role") == "Admin":
    menu_options.append("Profiles")
    menu_options.append("Database Check")

menu = st.sidebar.radio(
    "Menu", 
    menu_options
)

# ----------------------------------------
# --- PAGE ROUTING ---
# ----------------------------------------

if menu == "Home":
    render_home_page()
    
elif menu == "New Listing":
    st.header("Create a New Listing")
    tab_tool, tab_crop = st.tabs(["List a Tool", "List a Crop"])
    
    with tab_tool:
        render_tool_listing(st.session_state.get("farmer_name", ""))
    with tab_crop:
        render_crop_listing(st.session_state.get("farmer_name", ""))

elif menu == "View Listings":
    st.header("View and Manage Listings")
    tab1, tab2 = st.tabs(["Tools for Rent", "Crops for Sale"])

    with tab1:
        render_tool_management(st.session_state.tools, st.session_state.get("farmer_name", None))
    with tab2:
        render_crop_management(st.session_state.crops, st.session_state.get("farmer_name", None))

elif menu == "Profiles":
    render_profiles_page()

elif menu == "Database Check":
    render_db_check()
    
# ----------------------------------------
# --- FOOTER ---
# ----------------------------------------
st.markdown("""
<hr style='border-top: 2px solid #3CB371; margin-top: 30px;'>
<div style='text-align:center;color:#696969;padding:10px;'>
    <small>© 2025 Smart Farmer Marketplace | Prototype by Team AgroLink</small>
</div>
""", unsafe_allow_html=True)