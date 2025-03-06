import streamlit as st
from config import API_URL
from utils.api_helper import send_get_request, send_post_request
import time
import pandas as pd

def show_page():
    st.header("🏪 Manage Shops (Demands)")

    # 🔄 Fetch Current Shop Demands
    st.subheader("📋 Edit Shop Demands")
    response = send_get_request(f"{API_URL}/get_data")

    if response.status_code == 200:
        shop_data = response.json().get("shop_demands", {})

        if shop_data:
            st.write("### 🔢 Shop Demands Overview")

            # Convert to DataFrame for UI display
            shop_df = pd.DataFrame(list(shop_data.items()), columns=["Shop Name", "Demand"])

            # # 🔹 Use `st.form` to batch edit, but make "Shop Name" **read-only**
            with st.form(key="edit_shop_form"):
                edited_shop_df = st.data_editor(
                    shop_df, 
                    key="shop_demand_editor",
                    disabled=["Shop Name"],  # ⛔ Prevent editing shop names
                )
                submit_changes = st.form_submit_button("💾 Save Changes")
            # 🛠 Process Save Updates
            if submit_changes:
                errors = []
                for _, row in edited_shop_df.iterrows():
                    shop_name = row["Shop Name"]
                    new_demand = int(row["Demand"])

                    update_response = send_post_request(
                        f"{API_URL}/edit_shop_demand",
                        data={"shop_name": shop_name, "shop_demand": new_demand}, 
                    )

                    if update_response.status_code != 200:
                        errors.append(f"❌ Error updating {shop_name}: {update_response.json().get('detail', 'Unknown error')}")

                # ✅ Show results
                if not errors:
                    st.success("✅ Shop demands updated successfully!")
                    time.sleep(1)
                    st.rerun()  # Refresh UI
                else:
                    for err in errors:
                        st.error(err)
        else:
            st.write("⚠️ No shop demands found. Upload data first.")

    # 🔄 Refresh button
    if st.button("🔄 Refresh Shop List"):
        st.rerun()
