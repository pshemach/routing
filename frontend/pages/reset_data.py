import streamlit as st
from config import API_URL
from utils.api_helper import send_delete_request

# 🟢 RESET ALL DATA SECTION
def show_page():
    st.header("⚠️ Reset All Data")
    
    if st.button("Reset Data"):
        response = send_delete_request(f"{API_URL}/reset_data")
        if response.status_code == 200:
            st.success("✅ Data reset successfully!")
        else:
            st.error(f"❌ Error: {response.json()['detail']}")