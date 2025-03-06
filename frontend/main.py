# main.py
import streamlit as st
from config import API_URL
from pages import update_vehicles, update_shops, restricted_paths, solve_tsp, solve_vrp, view_data, reset_data
from pages.upload_data import upload_data_ui

# Streamlit App Title
st.title("🚚 TSP & VRP Solver")

# Sidebar Navigation
menu = st.sidebar.radio(
    "Navigation",
    ["Upload Data", "Manage Vehicles", "Manage Shops", "Manage Restrictions", "Solve TSP", "Solve VRP", "View Data", "Reset"]
)

# Route to corresponding module
if menu == "Upload Data":
    upload_data_ui()
elif menu == "Manage Vehicles":
    update_vehicles.show_page()
elif menu == "Manage Shops":
    update_shops.show_page()
elif menu == "Manage Restrictions":
    restricted_paths.show_page()
elif menu == "Solve TSP":
    solve_tsp.show_page()
elif menu == "Solve VRP":
    solve_vrp.show_page()
elif menu == "View Data":
    view_data.show_page()
elif menu == "Reset":
    reset_data.show_page()
