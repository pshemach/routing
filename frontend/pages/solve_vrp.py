import streamlit as st
from config import API_URL
from utils.api_helper import send_post_request
def show_page():
    st.header("🚛 Solve VRP (Vehicle Routing Problem)")
    
    if st.button("Solve VRP"):
        response = send_post_request(f"{API_URL}/solve_vrp")
        if response.status_code == 200:
            vrp_result = response.json()
            st.success("✅ VRP Solved Successfully!")
            
            for vehicle, details in vrp_result['routes'].items():
                st.subheader(f"🚚 {vehicle}")
                st.write(f"**Route:** {details['route']}")
                st.write(f"**Total Distance:** {details['total_distance']} km")
                st.write(f"**Total Load:** {details['total_load']} units")
        else:
            st.error(f"❌ Error: {response.json()['detail']}")