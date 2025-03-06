# utils/api_helpers.py
import requests
import time
import streamlit as st

def send_post_request(endpoint, data=None, files=None):
    """ Send POST request to API. """
    try:
        response = requests.post(endpoint, json=data, files=files)
        return response
    except Exception as e:
        st.error(f"⚠️ API Request Failed: {e}")
        return None

def send_get_request(endpoint):
    """ Send GET request to API. """
    try:
        response = requests.get(endpoint)
        return response
    except Exception as e:
        st.error(f"⚠️ API Request Failed: {e}")
        return None

def send_delete_request(endpoint, data=None):
    """ Send DELETE request to API. """
    try:
        response = requests.delete(endpoint, json=data)
        return response
    except Exception as e:
        st.error(f"⚠️ API Request Failed: {e}")
        return None
