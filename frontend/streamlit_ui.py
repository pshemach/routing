# import streamlit as st
# import requests
# import pandas as pd
# import io
# import time


# # API Base URL
# API_URL = "http://127.0.0.1:8088"  # Change if running API on a different host

# st.title("🚚 TSP & VRP Solver")

# # Sidebar for navigation
# menu = st.sidebar.radio("Navigation", ["Upload Data", "Manage Vehicles", "Manage Shops", "Manage Restrictions", "Solve TSP", "Solve VRP", "View Data", "Reset"])

# # 🟢 UPLOAD DATA SECTION
# if menu == "Upload Data":
#     st.header("📂 Upload CSV File")

#     # File uploader
#     uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
    
#     # Submit button to trigger the upload
#     if uploaded_file:
#         st.write(f"📄 Selected File: **{uploaded_file.name}**")  # Show the selected file name
    
#         if st.button("Upload File"):
#             try:
#                 # Display loading spinner
#                 with st.spinner("🚀 Uploading file... Please wait."):
#                     progress_bar = st.progress(0)  # Create a progress bar

#                     # Convert Streamlit file to bytes
#                     file_bytes = uploaded_file.read()
#                     files = {"file": ("data.csv", io.BytesIO(file_bytes), "text/csv")}

#                     # Simulate progress bar for better UI feedback
#                     for percent in range(0, 101, 10):
#                         time.sleep(2)  # Simulate upload time
#                         progress_bar.progress(percent)

#                     # Send file to backend
#                     response = requests.post(f"{API_URL}/upload_data", files=files)
                    
#                     progress_bar.progress(100)  # Mark as complete
                    
#                     if response.status_code == 200:
#                         st.success("✅ Data uploaded successfully!")
#                     else:
#                         st.error(f"❌ Error: {response.json().get('detail', 'Unknown error')}")

#             except Exception as e:
#                 st.error(f"⚠️ Unexpected error: {e}")
# # 🟢 MANAGE VEHICLES SECTION
# elif menu == "Manage Vehicles":
#     st.header("🚛 Manage Vehicles")
    
#     # Fetch current vehicles
#     st.subheader("📋 Current Vehicles")
#     vehicles_response = requests.get(f"{API_URL}/get_data")
    
#     if vehicles_response.status_code == 200:
#         vehicles_data = vehicles_response.json().get("vehicle_capacities", {})
        
#         if vehicles_data:
#             for v_name, v_capacity in vehicles_data.items():
#                 st.write(f"🚗 **{v_name}** - Capacity: `{v_capacity}`")
#         else:
#             st.write("⚠️ No vehicles added yet.")

#     # 🔄 Refresh button
#     if st.button("🔄 Refresh Vehicle List"):
#         st.rerun()  

#     # ➕ Add Vehicle
#     st.subheader("➕ Add Vehicle")
#     vehicle_name = st.text_input("Vehicle Name")
#     vehicle_capacity = st.number_input("Vehicle Capacity", min_value=1, step=1)
    
#     if st.button("Add Vehicle"):
#         if vehicle_name != '':
#             response = requests.post(f"{API_URL}/add_vehicle", params={"vehicle_name": vehicle_name, "vehicle_capacity": vehicle_capacity})
#             if response.status_code == 200:
#                 st.success("✅ Vehicle added successfully!")
#                 st.rerun()  
#             else:
#                 st.error(f"❌ Error: {response.json().get('detail', 'Unknown error')}")
#         else:
#             st.error("���️ Vehicle name cannot be empty.")

#     # 🗑 Remove Vehicle
#     st.subheader("🗑 Remove Vehicle")
#     vehicle_name_remove = st.selectbox("Select Vehicle to Remove", options=list(vehicles_data.keys()), index=0) if vehicles_data else None
    
#     if vehicle_name_remove and st.button("Remove Vehicle"):
#         response = requests.delete(f"{API_URL}/remove_vehicle", params={"vehicle_name": vehicle_name_remove})
#         if response.status_code == 200:
#             st.success(f"✅ Vehicle '{vehicle_name_remove}' removed successfully!")
#             st.rerun()  # ✅ Use this instead of st.experimental_rerun()
#         else:
#             st.error(f"❌ Error: {response.json().get('detail', 'Unknown error')}")


# # 🟢 MANAGE SHOPS (DEMANDS) SECTION
# elif menu == "Manage Shops":
#     st.header("🏪 Manage Shops (Demands)")

#     # 🔄 Fetch Current Shop Demands
#     st.subheader("📋 Edit Shop Demands")
#     response = requests.get(f"{API_URL}/get_data")

#     if response.status_code == 200:
#         shop_data = response.json().get("shop_demands", {})

#         if shop_data:
#             st.write("### 🔢 Shop Demands Overview")

#             # Convert to DataFrame for UI display
#             shop_df = pd.DataFrame(list(shop_data.items()), columns=["Shop Name", "Demand"])

#             # # 🔹 Use `st.form` to batch edit, but make "Shop Name" **read-only**
#             with st.form(key="edit_shop_form"):
#                 edited_shop_df = st.data_editor(
#                     shop_df, 
#                     key="shop_demand_editor",
#                     disabled=["Shop Name"],  # ⛔ Prevent editing shop names
#                 )
#                 submit_changes = st.form_submit_button("💾 Save Changes")
#             # 🛠 Process Save Updates
#             if submit_changes:
#                 errors = []
#                 for _, row in edited_shop_df.iterrows():
#                     shop_name = row["Shop Name"]
#                     new_demand = int(row["Demand"])

#                     update_response = requests.post(
#                         f"{API_URL}/edit_shop_demand",
#                         json={"shop_name": shop_name, "shop_demand": new_demand}, 
#                     )

#                     if update_response.status_code != 200:
#                         errors.append(f"❌ Error updating {shop_name}: {update_response.json().get('detail', 'Unknown error')}")

#                 # ✅ Show results
#                 if not errors:
#                     st.success("✅ Shop demands updated successfully!")
#                     time.sleep(2)
#                     st.rerun()  # Refresh UI
#                 else:
#                     for err in errors:
#                         st.error(err)
#         else:
#             st.write("⚠️ No shop demands found. Upload data first.")

#     # 🔄 Refresh button
#     if st.button("🔄 Refresh Shop List"):
#         st.rerun()



# # 🟢 MANAGE RESTRICTIONS SECTION
# elif menu == "Manage Restrictions":
#     st.header("🚧 Manage Restrictions")

#     # 🔄 Fetch current data
#     response = requests.get(f"{API_URL}/get_data")

#     if response.status_code == 200:
#         data = response.json()
#         locations = data.get("locations", [])
#         restricted_roads = data.get("restricted_roads", [])
#     else:
#         locations = []
#         restricted_roads = []
#         st.error("⚠️ Error fetching data. Please upload data first.")

#     # 🚧 **View Existing Restricted Roads**
#     st.subheader("📌 Existing Restricted Roads")
#     if restricted_roads:
#         for road in restricted_roads:
#             st.write(f"🔴 **{road[0]} ➝ {road[1]}**")
#     else:
#         st.info("No restricted roads added yet.")

#     # ➕ **Add Restricted Road**
#     st.subheader("➕ Add Restricted Road")
#     if locations:
#         start_location = st.selectbox("Start Location", locations, key="add_start_location")
#         end_location = st.selectbox("End Location", locations, key="add_end_location")

#         if st.button("Add Restricted Road"):
#             response = requests.post(
#                 f"{API_URL}/add_restricted_road",
#                 json={"start_location": start_location, "end_location": end_location},
#             )
#             if response.status_code == 200:
#                 st.success("✅ Restricted road added successfully!")
#                 st.rerun()  # Refresh UI
#             else:
#                 st.error(f"❌ Error: {response.json().get('detail', 'Unknown error')}")
#     else:
#         st.warning("⚠️ No locations available. Please upload data first.")

#     # 🗑 **Remove Restricted Road**
#     st.subheader("🗑 Remove Restricted Road")
#     if restricted_roads:
#         selected_road = st.selectbox("Select a Restricted Road to Remove", [f"{road[0]} ➝ {road[1]}" for road in restricted_roads])

#         if st.button("Remove Restricted Road"):
#             start_location_remove, end_location_remove = selected_road.split(" ➝ ")
#             response = requests.delete(
#                 f"{API_URL}/remove_restricted_road",
#                 json={"start_location": start_location_remove, "end_location": end_location_remove},
#             )
#             if response.status_code == 200:
#                 st.success("✅ Restricted road removed successfully!")
#                 st.rerun()  # Refresh UI
#             else:
#                 st.error(f"❌ Error: {response.json().get('detail', 'Unknown error')}")
#     else:
#         st.info("No restricted roads to remove.")



# # 🟢 SOLVE TSP SECTION
# elif menu == "Solve TSP":
#     st.header("🛤 Solve TSP (Traveling Salesman Problem)")
    
#     if st.button("Solve TSP"):
#         response = requests.post(f"{API_URL}/solve_tsp")
#         if response.status_code == 200:
#             tsp_result = response.json()
#             st.success(f"✅ Route: {tsp_result['route_order']}")
#             st.info(f"📏 Total Distance: {tsp_result['total_distance']} km")
#         else:
#             st.error(f"❌ Error: {response.json()['detail']}")

# # 🟢 SOLVE VRP SECTION
# elif menu == "Solve VRP":
#     st.header("🚛 Solve VRP (Vehicle Routing Problem)")
    
#     if st.button("Solve VRP"):
#         response = requests.post(f"{API_URL}/solve_vrp")
#         if response.status_code == 200:
#             vrp_result = response.json()
#             st.success("✅ VRP Solved Successfully!")
            
#             for vehicle, details in vrp_result['routes'].items():
#                 st.subheader(f"🚚 {vehicle}")
#                 st.write(f"**Route:** {details['route']}")
#                 st.write(f"**Total Distance:** {details['total_distance']} km")
#                 st.write(f"**Total Load:** {details['total_load']} units")
#         else:
#             st.error(f"❌ Error: {response.json()['detail']}")

# # 🟢 VIEW DATA SECTION
# elif menu == "View Data":
#     st.header("📊 View Data")
    
#     response = requests.get(f"{API_URL}/get_data")
#     if response.status_code == 200:
#         data = response.json()
#         st.json(data)
#     else:
#         st.error(f"❌ Error: {response.json()['detail']}")

# # 🟢 RESET ALL DATA SECTION
# elif menu == "Reset":
#     st.header("⚠️ Reset All Data")
    
#     if st.button("Reset Data"):
#         response = requests.delete(f"{API_URL}/reset_data")
#         if response.status_code == 200:
#             st.success("✅ Data reset successfully!")
#         else:
#             st.error(f"❌ Error: {response.json()['detail']}")

