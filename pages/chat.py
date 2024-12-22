import streamlit as st
from pages.multiagent.graph import EssayWriter
from elevenlabs import play, Voice, VoiceSettings
from elevenlabs.client import ElevenLabs
from modules.translator import translate_text
import base64

def text_to_speech(text):
    client = ElevenLabs(
        api_key=st.secrets["ELEVEN_API_KEY"],
    )
    audio = client.generate(
        text=text,
        voice=Voice(
            voice_id='cgSgspJ2msm6clMCkdW9',
            settings=VoiceSettings(stability=0.50, similarity_boost=0.60, style=0.0, use_speaker_boost=False)
        ),
        model="eleven_turbo_v2_5",
    )
    play(audio)

def chat_page():
    st.title("Sophie 👩🏼‍🦰")

    st.session_state.essaywriter = EssayWriter()
    #st.session_state.app = st.session_state.essaywriter.graph

    # Initialize session state for messages
    if "messages" not in st.session_state:
        # Checking if there's article content to include in the context
        if 'article_content' in st.session_state and 'article_title' in st.session_state:
            article_context = f"You have been provided with the following article titled '{st.session_state['article_title']}':\n\n{st.session_state['article_content']}\n\nYou should use this information to answer any questions."
            first_response = "Hi, I'm Sophie! You can ask me questions based on the article."
            first_response = first_response if st.session_state.language == "English" else translate_text(first_response)
            st.session_state.messages = [
                {"role": "assistant", "content": first_response},
                {"role": "system", "content": article_context}
            ]
            if st.session_state.tts_enabled:
                text_to_speech(first_response)
            st.session_state.essaywriter.memory.save_context(inputs={"input": article_context}, 
                                                     outputs={"output": first_response})
            st.session_state.report_essay = article_context
            st.session_state.app = None
            st.session_state.chat_active = False   
            
            # Clearing the article content after using it
            del st.session_state['article_content']
            del st.session_state['article_title']
        else:
            first_response = "Hi, I'm Sophie! How may I help you?"
            first_response = first_response if st.session_state.language == "English" else translate_text(first_response)
            st.session_state.messages = [{"role": "assistant", "content": first_response}]
            if st.session_state.tts_enabled:
                text_to_speech(first_response)
            st.session_state.app = None
            st.session_state.chat_active = False        

    st.divider()

    # app = st.session_state.app
    # def generate_response(topic):
        # return app.invoke(input={"topic": topic})
        # return st.session_state.essaywriter.generate_response(topic)

    # Display chat messages from history
    for message in st.session_state.messages:
        if message["role"] in ["assistant", "user"]:
            avatar = '👩🏼‍🦰' if message["role"] == "assistant" else '👨‍💻'
            with st.chat_message(message["role"], avatar=avatar):
                st.markdown(message["content"], unsafe_allow_html=True)

    if topic:= st.chat_input(placeholder="Ask a question", disabled=st.session_state.chat_active):
        st.chat_message("user", avatar="👨‍💻").markdown(topic)

        st.session_state.messages.append({"role": "user", "content": topic})
        with st.spinner("Lemme think..."):
            response = st.session_state.essaywriter.generate_response(topic)

        with st.chat_message("assistant", avatar="👩🏼‍🦰"):
            if "pdf_name" in response:
                with open(f"./{response['pdf_name']}", "rb") as file:
                    file_bytes = file.read()
                    b64 = base64.b64encode(file_bytes).decode()
                href = f"<a href='data:application/octet-stream;base64,{b64}' download='{response['pdf_name']}'>Click here to download the PDF Report</a>"

                st.markdown(f"{response['response']}: {href}", unsafe_allow_html=True)
                st.session_state.messages.append({"role": "assistant", "content": f"{response['response']}: {href}"})
            else:
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
                if st.session_state.tts_enabled and len(response) < 150:
                    text_to_speech(response)

if __name__ == "__main__":
    chat_page()