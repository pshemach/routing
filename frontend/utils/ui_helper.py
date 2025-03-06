# utils/ui_helpers.py
import streamlit as st
import time

def show_loading_spinner(duration=2):
    """ Display a loading spinner for UI feedback. """
    with st.spinner("Processing... Please wait."):
        time.sleep(duration)
