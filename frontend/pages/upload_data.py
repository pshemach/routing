# pages/upload_data.py
import streamlit as st
import io
import time
from config import API_URL
from frontend.utils.api_helper import send_post_request

def upload_data_ui():
    st.header("📂 Upload CSV File")

    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
    
    if uploaded_file:
        st.write(f"📄 Selected File: **{uploaded_file.name}**")

        if st.button("Upload File"):
            with st.spinner("🚀 Uploading file... Please wait."):
                progress_bar = st.progress(0)

                file_bytes = uploaded_file.read()
                files = {"file": ("data.csv", io.BytesIO(file_bytes), "text/csv")}

                for percent in range(0, 101, 10):
                    time.sleep(1)
                    progress_bar.progress(percent)

                response = send_post_request(f"{API_URL}/upload_data", files=files)

                progress_bar.progress(100)

                if response and response.status_code == 200:
                    st.success("✅ Data uploaded successfully!")
                else:
                    st.error(f"❌ Error: {response.json().get('detail', 'Unknown error')}")
