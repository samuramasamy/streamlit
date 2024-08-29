import streamlit as st
import httpx
import pandas as pd

API_URL = "http://127.0.0.1:8000"

def create_item(name, age, mobile_no, gender):
    response = httpx.post(f"{API_URL}/items/", json={"name": name, "age": age, "mobile_no": mobile_no, "gender": gender})
    return response.json()

def get_items():
    response = httpx.get(f"{API_URL}/items/")
    return response.json()

def get_item(name):
    response = httpx.get(f"{API_URL}/items/{name}")
    return response.json()

def edit_item(name, age, mobile_no, gender):
    response = httpx.put(f"{API_URL}/items/{name}", json={"name": name, "age": age, "mobile_no": mobile_no, "gender": gender})
    return response.json()

def delete_item(name):
    response = httpx.delete(f"{API_URL}/items/{name}")
    return response.json()

st.title("Application Form")

# Create
st.header("Create Application")
name = st.text_input("Name")
age = st.number_input("Age", min_value=0)
mobile_no = st.text_input("Mobile No")
gender = st.selectbox("Gender", ["Male", "Female", "Other"])

if st.button("Create"):
    response = create_item(name, age, mobile_no, gender)
    if response.get("detail") == "Item already exists":
        st.warning(f"Item '{name}' already exists.")
    else:
        st.success(f"Created {name}")
        st.balloons()
        # Reload the page or update the state manually
        st.session_state.update({"refresh": True})

# Sidebar for Read Items
st.sidebar.header("Read Application")
items = get_items()
if items:
    # Convert items to DataFrame for table display
    df = pd.DataFrame(items)
    st.sidebar.dataframe(df)
else:
    st.sidebar.write("No items found.")

# Edit
st.header("Edit Application")
if items:
    # List of item names for selection
    item_names = [item["name"] for item in items]
    update_name = st.selectbox("Select Item to Update", item_names, key="update_name")
    
    if update_name:
        # Get current item details
        item = get_item(update_name)
        if item:
            new_age = st.number_input("New Age", min_value=0, value=item['age'], key="update_age")
            new_mobile_no = st.text_input("New Mobile No", value=item['mobile_no'], key="update_mobile_no")
            new_gender = st.selectbox("New Gender", ["Male", "Female", "Other"], 
                                      index=["Male", "Female", "Other"].index(item['gender']), 
                                      key="update_gender")

            if st.button("Edit"):
                edit_response = edit_item(update_name, new_age, new_mobile_no, new_gender)
                if 'detail' in edit_response and edit_response['detail'] == "Item not found":
                    st.error(f"Item '{update_name}' not found.")
                else:
                    st.success(f"Edited item {update_name}")
                    # Reload the page or update the state manually
                    st.session_state.update({"refresh": True})
        else:
            st.error(f"Failed to retrieve details for item '{update_name}'.")
else:
    st.write("No items available for update.")

# Delete

st.sidebar.header("Delete Datas")
if items:
    delete_name = st.sidebar.selectbox("Select Item to Delete", [item["name"] for item in items], key="delete_name")

    if st.sidebar.button("Delete"):
        delete_item(delete_name)
        st.success(f"Deleted item {delete_name}")
        # Reload the page or update the state manually
        st.session_state.update({"refresh": True})
else:
    st.sidebar.write("No items available for deletion.")
