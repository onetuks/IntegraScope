import streamlit as st

from app.client.ui import hide_sidebar_nav, render_sidebar_nav

st.set_page_config(page_title="i-Scope", layout="wide")

hide_sidebar_nav()
render_sidebar_nav()

st.title("i-Scope")
