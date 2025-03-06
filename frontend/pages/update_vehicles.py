# pages/manage_vehicles.py
import streamlit as st
from config import API_URL
from utils.api_helper import send_get_request, send_post_request, send_delete_request

def show_page():
    st.header("🚛 Manage Vehicles")
    
    # Fetch current vehicles
    st.subheader("📋 Current Vehicles")
    vehicles_response = send_get_request(f"{API_URL}/get_data")
    
    if vehicles_response.status_code == 200:
        vehicles_data = vehicles_response.json().get("vehicle_capacities", {})
        
        if vehicles_data:
            for v_name, v_capacity in vehicles_data.items():
                st.write(f"🚗 **{v_name}** - Capacity: `{v_capacity}`")
        else:
            st.write("⚠️ No vehicles added yet.")

    # 🔄 Refresh button
    if st.button("🔄 Refresh Vehicle List"):
        st.rerun()  

    # ➕ Add Vehicle
    st.subheader("➕ Add Vehicle")
    vehicle_name = st.text_input("Vehicle Name")
    vehicle_capacity = st.number_input("Vehicle Capacity", min_value=1, step=1)
    
    if st.button("Add Vehicle"):
        if vehicle_name != '':
            response = send_post_request(f"{API_URL}/add_vehicle", data={"vehicle_name": vehicle_name, "vehicle_capacity": vehicle_capacity})
            if response.status_code == 200:
                st.success("✅ Vehicle added successfully!")
                st.rerun()  
            else:
                st.error(f"❌ Error: {response.json().get('detail', 'Unknown error')}")
        else:
            st.error("���️ Vehicle name cannot be empty.")

    # 🗑 Remove Vehicle
    st.subheader("🗑 Remove Vehicle")
    vehicle_name_remove = st.selectbox("Select Vehicle to Remove", options=list(vehicles_data.keys()), index=0) if vehicles_data else None
    
    if vehicle_name_remove and st.button("Remove Vehicle"):
        response = send_delete_request(f"{API_URL}/remove_vehicle", data={"vehicle_name": vehicle_name_remove})
        if response.status_code == 200:
            st.success(f"✅ Vehicle '{vehicle_name_remove}' removed successfully!")
            st.rerun()  # ✅ Use this instead of st.experimental_rerun()
        else:
            st.error(f"❌ Error: {response.json().get('detail', 'Unknown error')}")

