import streamlit as st
from streamlit_lottie import st_lottie
from modules.cache_functions import cache_banner
from modules.constants import LANGUAGES

def home_page():
    with st.columns([1, 2, 1])[1]:
        st.image(cache_banner(), use_column_width="auto")

    st.write(
        """
        <center>
            <h2>Welcome to app_v2!<br/>Omdena's Crisis Forecasting Tool Project for ACAPS</h2>
            <p>This project aims to develop a custom workflow that leverages AI-powered tools to gather real-time data on crisis triggers. By utilizing data from multiple sources such as Twitter, Google Trends, and news websites, we categorize public sentiment and provide actionable insights for data analysts and policymakers in various countries. Our goal is to offer precise, real-time information to support informed decision-making to predict crisis situations.</p>
        </center>
        <br/><br/><br/><br/><br/><br/><br/><br/><br/><hr>
        <h4>New Features in app_v2! 🤩</h4>
        <ul>
            <li><strong>Sophie</strong> is now available in more than 20 languages. To change language, please scroll down.</li>
            <li><strong>Sophie</strong> can now reply with voice for short messages, in <em>all</em> those 20+ languages. To toggle voice mode on or off, please scroll down.</li>
            <li>A brand new <strong>ACLED Data Explorer page</strong>, where you can browse through ACLED's data and also get advanced AI-based summaries and key points.</li>
            <li><strong>ACLED Data has been integrated</strong> with Sophie, so she can perform analysis on country-specific ACLED Data as well.</li>
            <li><strong>Completely revamped query routing mechanism</strong> for Sophie so she can better detect what you are asking for and respond accordingly with facts and data.</li>
            <li><strong>GDELT and Twitter agents</strong> in the chat system are also <strong>fully functional</strong> for the country of Ukraine. Support for more countries will be added in the future, due to restrictions in the usage of their API.</li>
            <li><strong>Sophie can now remember country-specific inquiry responses</strong> of all agents as context, to give you better replies in a conversation. In v1, Sophie only remembered the summary that was displayed to you, the user.</li>
        </ul>
        <hr>
        <br/>
        """,
        unsafe_allow_html=True,
    )

    with st.container():
        col1, col2 = st.columns([1, 1])
        def_index = LANGUAGES.index(st.session_state.language) if 'language' in st.session_state else 0
        
        with col1:
            language = st.selectbox(
                'Choose Sophie\'s Language',
                LANGUAGES,
                index=def_index
            )

        with col2:
            if 'tts_enabled' in st.session_state:
                tts_enabled = st.checkbox('Enable Voice Mode', value=st.session_state.tts_enabled)
            else:
                tts_enabled = st.checkbox('Enable Voice Mode', value=True)

    st.session_state.language = language
    st.session_state.tts_enabled = tts_enabled

    cols1 = st.columns([0.2, 1, 0.05, 1, 0.2])
    padding_row = "<br>"

    with cols1[1]:
        st.write(
            """
            <h3>Impact on Analysis and Decision Making</h3>
            <p>The slow pace and potential inaccuracies of manual sentiment analysis have significant implications for political analysis and decision-making in regions experiencing political, economic, and social unrest. Delays in obtaining real-time information hinder analysts and policymakers from proactively responding to public sentiment, leading to missed opportunities for engagement or intervention. Furthermore, inaccuracies in manual analysis can result in poorly informed strategies that not only fail to achieve objectives but also exacerbate public dissatisfaction and distrust, affecting political stability and undermining the democratic process.</p>
        """,
            unsafe_allow_html=True,
        )
        st.write(padding_row, unsafe_allow_html=True)

        st_lottie(
            "https://lottie.host/4bbcd636-eece-482f-8613-0e3ed93dafec/4ezAdnro3W.json",
            height=325,
        )
        st.write(padding_row, unsafe_allow_html=True)

        st.write(
            """
            <h3>Empowering Analysts with Real-Time Insights</h3>
            <p>The goal of this initiative is to provide analysts and policymakers in regions experiencing political, economic, and social unrest with real-time and accurate insights on public sentiment. By utilizing an advanced web interface to gather and visualize data from sources like Twitter, Google Trends, and news websites, the project enhances the ability to quickly respond to crises and improve the effectiveness of strategies and policies.</p>
        """, 
            unsafe_allow_html=True)

    with cols1[3]:
        st_lottie(
            "https://lottie.host/a786afd8-9903-4bed-8952-12b21b8016bd/PBO8x4JBEQ.json",
            height=325,
        )
        st.write(padding_row, unsafe_allow_html=True)

        st.write(
            f"""
            <br>
            <h3>The Need for an Automated Solution</h3>
            <p>The development of an AI-powered sentiment analysis tool is essential to overcoming the challenges of manual analysis. By applying advanced Natural Language Processing (NLP) techniques to various data sources, this tool provides a faster and more accurate process, enabling timely insights in response to emerging crises.</p>
            {'<br>'*5}
        """,
            unsafe_allow_html=True,
        )
        st.write(padding_row, unsafe_allow_html=True)

        st_lottie(
            "https://lottie.host/9c945dc7-e5d7-4148-b7f6-dfd748e1eb38/q0oJidkFyf.json",
            height=325,
        )

