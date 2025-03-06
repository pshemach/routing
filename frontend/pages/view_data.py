import streamlit as st
from config import API_URL
from utils.api_helper import send_get_request

def show_page():
    st.header("📊 View Data")
    response = send_get_request(f"{API_URL}/get_data")
    
    if response.status_code == 200:
        data = response.json()
        st.json(data)
    else:
        st.error(f"❌ Error: {response.json()['detail']}")
