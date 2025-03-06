import streamlit as st
from config import API_URL
from utils.api_helper import send_post_request

def show_page():
    st.header("🛤 Solve TSP (Traveling Salesman Problem)")
    
    if st.button("Solve TSP"):
        response = send_post_request(f"{API_URL}/solve_tsp")
        if response.status_code == 200:
            tsp_result = response.json()
            st.success(f"✅ Route: {tsp_result['route_order']}")
            st.info(f"📏 Total Distance: {tsp_result['total_distance']} km")
        else:
            st.error(f"❌ Error: {response.json()['detail']}")