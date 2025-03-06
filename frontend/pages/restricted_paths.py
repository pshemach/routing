import streamlit as st
from config import API_URL
from utils.api_helper import send_get_request, send_post_request, send_delete_request

def show_page():
    st.header("🚧 Manage Restrictions")

    # 🔄 Fetch current data
    response = send_get_request(f"{API_URL}/get_data")

    if response.status_code == 200:
        data = response.json()
        locations = data.get("locations", [])
        restricted_roads = data.get("restricted_roads", [])
    else:
        locations = []
        restricted_roads = []
        st.error("⚠️ Error fetching data. Please upload data first.")

    # 🚧 **View Existing Restricted Roads**
    st.subheader("📌 Existing Restricted Roads")
    if restricted_roads:
        for road in restricted_roads:
            st.write(f"🔴 **{road[0]} ➝ {road[1]}**")
    else:
        st.info("No restricted roads added yet.")

    # ➕ **Add Restricted Road**
    st.subheader("➕ Add Restricted Road")
    if locations:
        start_location = st.selectbox("Start Location", locations, key="add_start_location")
        end_location = st.selectbox("End Location", locations, key="add_end_location")

        if st.button("Add Restricted Road"):
            response = send_post_request(
                f"{API_URL}/add_restricted_road",
                json={"start_location": start_location, "end_location": end_location},
            )
            if response.status_code == 200:
                st.success("✅ Restricted road added successfully!")
                st.rerun()  # Refresh UI
            else:
                st.error(f"❌ Error: {response.json().get('detail', 'Unknown error')}")
    else:
        st.warning("⚠️ No locations available. Please upload data first.")

    # 🗑 **Remove Restricted Road**
    st.subheader("🗑 Remove Restricted Road")
    if restricted_roads:
        selected_road = st.selectbox("Select a Restricted Road to Remove", [f"{road[0]} ➝ {road[1]}" for road in restricted_roads])

        if st.button("Remove Restricted Road"):
            start_location_remove, end_location_remove = selected_road.split(" ➝ ")
            response = send_delete_request(
                f"{API_URL}/remove_restricted_road",
                json={"start_location": start_location_remove, "end_location": end_location_remove},
            )
            if response.status_code == 200:
                st.success("✅ Restricted road removed successfully!")
                st.rerun()  # Refresh UI
            else:
                st.error(f"❌ Error: {response.json().get('detail', 'Unknown error')}")
    else:
        st.info("No restricted roads to remove.")
