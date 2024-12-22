from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import streamlit as st

def translate_text(response: str):
        model = ChatOpenAI(model="gpt-4o-mini", 
                           api_key=st.secrets["OPENAI_API_KEY"])
        translation_prompt = """
                            You are an expert translator. You know {language} language very well.
                            Now, you are required to translate the following text into {language} language, 
                            keeping the formatting and structure same.
                            Reply with the translated text only, without any additional information.
                            
                            \nText: {text}
                            """
        prompt = PromptTemplate.from_template(translation_prompt)
        chain = prompt | model | StrOutputParser()
        result = chain.invoke({"text": response, 
                               "language": st.session_state.language})
        return result