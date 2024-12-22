import streamlit as st
from st_on_hover_tabs import on_hover_tabs
from pages.home import home_page
from pages.analyse import analyse_page
from pages.dashboard import dashboard
from pages.about import about_us_page
from pages.reliefweb import reliefweb_page
from pages.fewsnet_map import fewsnet_page
from pages.chat import chat_page
from pages.acled import acled_page
from modules.constants import CONTRIBUTORS, DEFAULT_CHOICE
from modules.utils import load_header

def launch_sidebar():
    with st.sidebar:
        st.write("<br>" * 4, unsafe_allow_html=True)
        selected_task = on_hover_tabs(
            tabName=["Home Page", "Analyse Sentiment", "Dashboard", "Reliefweb Reports", "FEWSNET Reports", "ACLED Data", "Chat",  "About Us"],
            iconName=["home", "engineering", "equalizer", "report", "map", "security", "chat", "contact_support"],
            styles={
                "navtab": {"background-color": "#fff"},
                "tabOptionsStyle": {
                    ":hover :hover": {"color": "#170034", "cursor": "pointer"}
                },
            },
            default_choice=DEFAULT_CHOICE,
        )
    if selected_task == "Home Page":
        with st.spinner("Loading main page..."):
            home_page()
    elif selected_task == "Analyse Sentiment":
        with st.spinner("Loading Analyze Tweet..."):
            analyse_page()
    elif selected_task == "Dashboard":
        if "master_df" in st.session_state and st.session_state["master_df"] is None:
            load_header("Dashboard")
            st.info("Please analyze a tweet before accessing the dashboard")
        else:
            with st.spinner("Loading dashboard..."):
                dashboard()
    elif selected_task == "About Us":
        with st.spinner("Loading About Us..."):
            about_us_page(CONTRIBUTORS)
    elif selected_task == "Reliefweb Reports":
        with st.spinner("Loading Reliefweb Reports..."):
            reliefweb_page()
    elif selected_task == "FEWSNET Reports":
        with st.spinner("Loading FEWSNET Reports..."):
            fewsnet_page()
    elif selected_task == "Chat":
        with st.spinner("Loading Chat..."):
            chat_page()
    elif selected_task == "ACLED Data":
        with st.spinner("Loading ACLED Data..."):
            acled_page()