import streamlit as st

from app.client.ui import hide_sidebar_nav, render_sidebar_nav

hide_sidebar_nav()
render_sidebar_nav("Case Search")

st.title("Case Search")
