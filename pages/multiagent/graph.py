import sys
__import__('pysqlite3')
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from langgraph.graph import StateGraph, END
from pydantic import Field, BaseModel
from typing import TypedDict, List, Dict, Any
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from pages.multiagent.pdf_writer import generate_pdf
from pages.multiagent.crew import CrewClass
from modules.translator import translate_text
import streamlit as st
import json, re

class GraphState(TypedDict):
    topic: str
    response: str
    documents: List[str]
    essay: Dict[str, Any]
    pdf_name: str

class EssayWriter:
    def __init__(self):
        self.model = ChatOpenAI(model="gpt-4o-mini",
                                api_key=st.secrets["OPENAI_API_KEY"])
        self.crew = CrewClass(llm=self.model)

        if 'memory' not in st.session_state:
            st.session_state.memory = ConversationBufferMemory()
            print("Initialized new ConversationBufferMemory in session state.")
        else:
            print("Loaded existing ConversationBufferMemory from session state.")

        self.memory = st.session_state.memory
        self.model = ChatOpenAI(model="gpt-4o-mini", 
                                api_key=st.secrets["OPENAI_API_KEY"])
        self.essay = ""

    def generate_response(self, user_input):
        # Get the response from the crew
        crew_response = self.crew.ultimate_kickoff(user_input, essay=self.essay)
        return_reponse, saved_response = "", ""

        # Ensure the response is a valid string
        if isinstance(crew_response, dict):
            return_reponse = saved_response = json.dumps(crew_response)
        elif isinstance(crew_response, tuple):
            saved_response, return_reponse = crew_response
        elif isinstance(crew_response, str):
            return_reponse = saved_response = crew_response
        else:
            return_reponse = saved_response = str(crew_response)

        self.essay = saved_response

        # Translation of the response
        return_reponse = translate_text(return_reponse)

        # Save conversation in memory
        print(f"**REPLY**\n{return_reponse}")
        self.memory.save_context(inputs={"input": user_input}, outputs={"output": saved_response})
        return return_reponse