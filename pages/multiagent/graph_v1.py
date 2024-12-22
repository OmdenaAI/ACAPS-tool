__import__('pysqlite3') # This is a workaround to fix the error "sqlite3 module is not found" on live streamlit.
import sys, re
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3') # This is a workaround to fix the error "sqlite3 module is not found" on live streamlit.

from langgraph.graph import StateGraph, END
from pydantic import BaseModel, Field
from typing import TypedDict, List, Literal, Dict, Any
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain_groq import ChatGroq
import streamlit as st
from pages.multiagent.pdf_writer import generate_pdf
from ACAPS.streamlit_app.pages.multiagent.crew_v1 import CrewClass, Essay
from langchain_openai import ChatOpenAI


class GraphState(TypedDict):
    topic: str
    response: str
    documents: List[str]
    essay: Dict[str, Any]
    pdf_name: str


class EssayWriter:
    def __init__(self):
        '''self.model = ChatGroq(model="llama3-8b-8192",
                              api_key=st.secrets["GROQ_API_KEY"])
        self.crew = CrewClass(llm=ChatGroq(model="groq/llama3-8b-8192",
                                           api_key=st.secrets["GROQ_API_KEY"]
                                        ))'''
        
        self.model = ChatOpenAI(model="gpt-4o-mini",
                                api_key=st.secrets["OPENAI_API_KEY"])
        self.crew = CrewClass(llm=ChatOpenAI(model="gpt-4o-mini",
                                             api_key=st.secrets["OPENAI_API_KEY"]))

        if 'memory' not in st.session_state:
            st.session_state.memory = ConversationBufferMemory()
            print("Initialized new ConversationBufferMemory in session state.")
        else:
            print("Loaded existing ConversationBufferMemory from session state.")

        if 'report_essay' not in st.session_state:
            st.session_state.report_essay = ""
            print("Initialized new report_essay.")
        else:
            print("Loaded existing report_essay.")
        
        self.memory = st.session_state.memory
        self.essay = {}
        self.router_prompt = """
                            You are a router and your duty is to route the user to the correct expert.
                            Always check conversation history and consider your move based on it.
                            The following points are based on preference from high to low.
                            1. If topic is something about memory, or daily talk, or a general task like summarisation or explanation then route the user to the answer expert.\n
                            2. If the user is asking to generate or write a report of anything, route to the write_report expert only.\n
                            3. If topic starts something like can you write, or user request you write a report or essay, route the user to the write_essay expert.\n
                            4. If the user wants to edit anything in the essay, route the user to the edit_essay expert.\n
                            5. If the user want to know about the google trends of a certain country or topic, route to the google_trends_analysis expert.\n
                            6. If the user wants to know about the GDELT data of a certain country or topic, route to the gdelt_analysis expert.\n
                            7. If the user is asking for crisis analysis or says something like "what is the ___ situation in ___" or "please tell me about the ___ crisis in ___" or 
                                tells you to fetch and show Twitter Data, GDELT Data or Google Trends Data, route to the crisis_analysis expert.\n
                            8. If topic requires fetching ReliefWeb reports, analysis of which aren't already present in the conversation (check history for that), route to the reliefweb_analysis expert.\n
                            9. If topic is anything regarding FEWSNET reports or the user wants an analysis of FEWSNET reports data, route to the fewsnet_analysis expert.\n

                            \nConservation History: {memory}
                            \nTopic: {topic}
                            """
                            
        self.simple_answer_prompt = """
                            You are an expert and you are providing a simple answer to the user's question.
                            
                            \nConversation History: {memory}
                            \nTopic: {topic}
                            """

        self.report_count_prompt = """
                            You are a simple person who reads the user's statement and provides the number of reports the user asks for.
                            Make sure that the response is an integer only, like "n" where n, the number of reports the user is asking for, an integer.
                            Do NOT return anything else other than the number (integer).
                            
                            \nConservation History: {memory}
                            \nTopic: {topic}
                            """
        
        self.general_param_filling_prompt = """
                            You are an expert at analysing chats. Go through the conversation history and the latest user query,
                            and fill in the required parameters for the task.\n
                            The parameters required and their details are as follows:\n
                                1. keyword: The keyword that the user is asking about. It could be anything like food, war, humanitarian, etc. Make sure that the keyword is a string type.\n
                                2. country: The country that the user is asking about. It could be any country like India, Ukraine, Somalia, etc. Make sure that the country is a string type.\n
                                3. number_of_reports: The number of reports the user is asking for. It could be any integer value. Make sure that the number of reports is an integer type.\n

                            If you are not at all able to figure our the parameters, then return " , , 0" which means "" for keyword and country, and 0 for number_of_reports. This should be your last resort.\n
                            Your response to this task should be in the format "keyword, country, number_of_reports" where keyword is the keyword, country is the country, and number_of_reports is the number of reports.\n
                            Do NOT return anything else other than what is asked of you. And MAKE SURE to adhere to the response format and their data types specified.\n
                            
                            \nConservation History: {memory}
                            \nLatest Prompt (by user): {topic}
                            """
        
        self.keyword_country_prompt = """
                            You are a simple person who reads the user's statement and provides the keyword and country the user asks for.
                            Make sure that the response is in the format "keyword, country" where keyword is the keyword and country is the country.
                            Do NOT return anything else other than the keyword and country in the specified format.

                            Some examples for your understanding: 
                                1. if the user asks "what is the food situation or crisis in India", then the response should be "food, India".
                                2. if the user asks "what is the war situation in Ukraine", then the response should be "war, Ukraine".
                                3. if the user asks "please give me information about the humanitarian crisis in Somalia", then the response should be "humanitarian, Somalia".
                                4. if the user asks "please tell me about the war situation in Ukraine", then the response should be "war, Ukraine".

                            Note that these are just example and not hard and fast rules. 
                            The user will input something along these lines.
                            You can provide the keyword and country based on the user's query.

                            \nConservation History: {memory}
                            \nTopic: {topic}
                            """

        builder = StateGraph(GraphState)

        builder.add_node("answer", self.answer)
        builder.add_node("write_essay", self.write_essay)
        builder.add_node("edit_essay", self.edit_essay)
        builder.add_node("write_report", self.write_report)
        builder.add_node("gdelt_analysis", self.gdelt_analysis)
        builder.add_node("ultimate_crew_analysis", self.ultimate_crew_analysis)
        builder.add_node("google_trends_analysis", self.google_trends_analysis)
        builder.add_node("crisis_analysis", self.crisis_analysis)
        builder.add_node("reliefweb_analysis", self.reliefweb_analysis)
        builder.add_node("fewsnet_analysis", self.fewsnet_analysis)

        builder.set_conditional_entry_point(
            self.router_query,
            {
                "write_essay": "write_essay",
                "write_report": "write_report",
                "edit_essay": "edit_essay",
                "gdelt_analysis": "gdelt_analysis",
                "google_trends_analysis": "google_trends_analysis",
                "crisis_analysis": "crisis_analysis",
                "reliefweb_analysis": "reliefweb_analysis",
                "fewsnet_analysis": "fewsnet_analysis",
                "answer": "answer",
                "ultimate_crew_analysis": "ultimate_crew_analysis"
            }
        )

        builder.add_edge("write_essay", END)
        builder.add_edge("edit_essay", END)
        builder.add_edge("answer", END)
        builder.add_edge("write_report", END)
        builder.add_edge("gdelt_analysis", END)
        builder.add_edge("ultimate_crew_analysis", END)
        builder.add_edge("google_trends_analysis", END)
        builder.add_edge("crisis_analysis", END)
        builder.add_edge("reliefweb_analysis", END)
        builder.add_edge("fewsnet_analysis", END)

        self.graph = builder.compile()
        self.graph.get_graph().draw_mermaid_png(output_file_path="graph.png")
        self.memory.save_context(inputs={"input": "You are Sophie, a lovely and helpful language model assistant."
                                                  "You are here to help me, the user with my queries."},
                                 outputs={"output": "Okay, sure! I am here to help you."})


    def router_query(self, state: GraphState):
        print("**ROUTER**")
        prompt = PromptTemplate.from_template(self.router_prompt)
        memory = self.memory.load_memory_variables({})
        chain = prompt | self.model
        response = chain.invoke({"topic": state["topic"], "memory": memory}).content
        print("Router Response:", response)
        
        # Extracting the routing decision from the response
        match = re.search(r'\b(edit_essay|write_essay|reliefweb_analysis|fewsnet_analysis|answer|write_report|crisis_analysis|gdelt_analysis|google_trends_analysis)\b', response)
        routing_option = match.group(1) if match else "answer"
        
        if routing_option == "reliefweb_analysis" or routing_option == "fewsnet_analysis":
            # Extracting number of reports if mentioned
            prompt = PromptTemplate.from_template(self.report_count_prompt)
            memory = self.memory.load_memory_variables({})
            chain = prompt | self.model
            response = chain.invoke({"topic": state["topic"], "memory": memory}).content
            print("Report Count Response:", response, "\n")
            st.session_state.number_of_reports = int(re.search(r'\d+', response).group()) if re.search(r'\d+', response) else 1
            state["number_of_reports"] = st.session_state.number_of_reports
        else:
            print("Number of reports not required for this task or could not be retrieved\n.")
            st.session_state.number_of_reports = 1
            state["number_of_reports"] = st.session_state.number_of_reports

        if routing_option == "crisis_analysis" or routing_option == "gdelt_analysis" or routing_option == "google_trends_analysis":
            # Extracting keyword and country
            prompt = PromptTemplate.from_template(self.keyword_country_prompt)
            memory = self.memory.load_memory_variables({})
            chain = prompt | self.model
            response = chain.invoke({"topic": state["topic"], "memory": memory}).content
            print("Keyword, Country:", response, "\n")
            st.session_state.keyword_country = tuple(response.split(", ")) if response else ("", "")
            if st.session_state.keyword_country[0] == "" or st.session_state.keyword_country[1] == "":
                routing_option = "answer"
            state["keyword_country"] = st.session_state.keyword_country
        
        print("Router Result: ", routing_option)
        return routing_option #"ultimate_crew_analysis"

    def answer(self, state: GraphState):
        print("**ANSWER**")
        prompt = PromptTemplate.from_template(self.simple_answer_prompt)
        memory = self.memory.load_memory_variables({})
        chain = prompt | self.model | StrOutputParser()
        result = chain.invoke({"topic": state["topic"], "memory": memory})

        self.memory.save_context(inputs={"input": state["topic"]}, outputs={"output": result})
        return {"response": result}

    def write_essay(self, state: GraphState):
        print("**ESSAY COMPLETION**")

        self.essay = self.crew.kickoff({"topic": state["topic"], "number_of_reports": state.get("number_of_reports", 1)})

        self.memory.save_context(inputs={"input": state["topic"]}, outputs={"output": str(self.essay)})

        pdf_name = generate_pdf(self.essay)
        return {"response": "Here is your essay! ",  "pdf_name": f"{pdf_name}"}

    def edit_essay(self, state: GraphState):
        print("**ESSAY EDIT**")
        memory = self.memory.load_memory_variables({})

        user_request = state["topic"]
        parser = JsonOutputParser(pydantic_object=Essay)
        prompt = PromptTemplate(
            template=("Edit the Json file as user requested, and return the new Json file."
                     "\n Request:{user_request} "
                     "\n Conservation History: {memory}"
                     "\n Json File: {essay}"
                     " \n{format_instructions}"),
            input_variables=["memory","user_request","essay"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )

        chain = prompt | self.model | parser
        self.essay = chain.invoke({"user_request": user_request, "memory": memory, "essay": self.essay})

        self.memory.save_context(inputs={"input": state["topic"]}, outputs={"output": str(self.essay)})
        pdf_name = generate_pdf(self.essay)
        return {"response": "Here is your edited essay! ", "essay": self.essay, "pdf_name": f"{pdf_name}"}

    def write_report(self, state: GraphState):
        print("**REPORT GENERATION**")

        essay_content = st.session_state.report_essay
        if not essay_content:
            return {"response": "Oopsies! Looks like Sophie hasn't written any essay yet."}

        # Use the LLM to convert the essay into the Essay JSON format
        parser = JsonOutputParser(pydantic_object=Essay)
        prompt = PromptTemplate(
            template=(
                "Convert the following essay into the given JSON format and return the new JSON file ONLY."
                "Do NOT exclude any information given to you.\n"
                "\nThe Essay Content:\n{essay_content}"
                "\n{format_instructions}"
            ),
            input_variables=["essay_content"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )

        chain = prompt | self.model | parser
        formatted_essay = chain.invoke({"essay_content": essay_content})
        print("**ESSAY CONTENT**\n", essay_content, "\n**FORMATTED ESSAY**\n", formatted_essay)
        pdf_name = generate_pdf(formatted_essay)

        self.memory.save_context(inputs={"input": state["topic"]}, outputs={"output": str(formatted_essay)})
        state["pdf_name"] = pdf_name
        state["essay"] = formatted_essay

        return {"response": "Here is your report!", "pdf_name": f"{pdf_name}", "essay": formatted_essay}

    # ReliefWeb Analysis
    def reliefweb_analysis(self, state: GraphState):
        print("**RELIEFWEB ANALYSIS**")
        
        # number_of_reports = state.get("number_of_reports", 1)
        self.crew.reliefweb_task.description = self.crew.reliefweb_task.description.format(number_of_reports=st.session_state.number_of_reports)
        # reliefweb_result = self.crew.reliefweb_kickoff({"number_of_reports": state.get("number_of_reports", 1)})
        max_retries = 10
        for attempt in range(max_retries):
            try:
                reliefweb_result = self.crew.reliefweb_kickoff({"number_of_reports": st.session_state.number_of_reports})
                break
            except ValueError as e:
                if str(e) == "Invalid response from LLM call - None or empty.":
                    if attempt == max_retries - 1:
                        reliefweb_result = "Unable to do the task!"
                else:
                    raise

        st.session_state.report_essay = reliefweb_result
        self.memory.save_context(inputs={"input": state["topic"]}, outputs={"output": str(reliefweb_result)})
        
        return {"response": f"Here is the analysis from ReliefWeb reports:\n\n{reliefweb_result}"}
    
    # FEWSNET Analysis
    def fewsnet_analysis(self, state: GraphState):
        print("**FEWSNET ANALYSIS**")
        
        # number_of_reports = state.get("number_of_reports", 1)
        # self.crew.fewsnet_task.description = self.crew.fewsnet_task.description.format(number_of_reports=number_of_reports)
        max_retries = 5
        for attempt in range(max_retries):
            try:
                fewsnet_result = self.crew.fewsnet_kickoff({"number_of_reports": st.session_state.number_of_reports})
                break
            except ValueError as e:
                if str(e) == "Invalid response from LLM call - None or empty.":
                    if attempt == max_retries - 1:
                        fewsnet_result = "Unable to do the task!"
                else:
                    raise

        st.session_state.report_essay = fewsnet_result
        self.memory.save_context(inputs={"input": state["topic"]}, outputs={"output": str(fewsnet_result)})
        
        return {"response": f"Here is the analysis from FEWSNET reports:\n\n{fewsnet_result}"}
    
    # Crisis Analysis
    def crisis_analysis(self, state: GraphState):
        print("**CRISIS ANALYSIS**")
        
        keyword, country = st.session_state.keyword_country
        
        max_retries = 5
        for attempt in range(max_retries):
            try:
                crisis_result = self.crew.crisis_kickoff({"keyword": keyword, "country": country})
                break
            except ValueError as e:
                if str(e) == "Invalid response from LLM call - None or empty.":
                    if attempt == max_retries - 1:
                        crisis_result = "Unable to do the task!"
                else:
                    raise

        st.session_state.report_essay = crisis_result
        self.memory.save_context(inputs={"input": state["topic"]}, outputs={"output": str(crisis_result)})
        
        return {"response": f"Here is the crisis analysis for the keyword '{keyword}' in '{country}':\n\n{crisis_result}"}
    
    # GDELT Analysis
    def gdelt_analysis(self, state: GraphState):
        print("**GDELT ANALYSIS**")
        
        keyword, country = st.session_state.keyword_country
        
        max_retries = 5
        for attempt in range(max_retries):
            try:
                gdelt_result = self.crew.gdelt_kickoff({"keyword": keyword, "country": country})
                break
            except ValueError as e:
                if str(e) == "Invalid response from LLM call - None or empty.":
                    if attempt == max_retries - 1:
                        gdelt_result = "Unable to do the task!"
                else:
                    raise

        st.session_state.report_essay = gdelt_result
        self.memory.save_context(inputs={"input": state["topic"]}, outputs={"output": str(gdelt_result)})
        
        return {"response": f"Here is the GDELT analysis for the keyword '{keyword}' in '{country}':\n\n{gdelt_result}"}
    
    # Google Trends Analysis
    def google_trends_analysis(self, state: GraphState):
        print("**GOOGLE TRENDS ANALYSIS**")
        
        keyword, country = st.session_state.keyword_country
        
        max_retries = 5
        for attempt in range(max_retries):
            try:
                google_trends_result = self.crew.google_trends_kickoff({"keyword": keyword, "country": country})
                break
            except ValueError as e:
                if str(e) == "Invalid response from LLM call - None or empty.":
                    if attempt == max_retries - 1:
                        google_trends_result = "Unable to do the task!"
                else:
                    raise

        st.session_state.report_essay = google_trends_result
        self.memory.save_context(inputs={"input": state["topic"]}, outputs={"output": str(google_trends_result)})
        
        return {"response": f"Here is the Google Trends analysis for the keyword '{keyword}' in '{country}':\n\n{google_trends_result}"}

    # Ultimate Crew Analysis where all agents are in one crew
    def ultimate_crew_analysis(self, state: GraphState):
        print("**ULTIMATE CREW ANALYSIS**")
        
        prompt = PromptTemplate.from_template(self.general_param_filling_prompt)
        memory = self.memory.load_memory_variables({})
        chain = prompt | self.model
        response = chain.invoke({"topic": state["topic"], "memory": memory}).content
        print("Params. :'", response, "'\n")
        general_params_tuple = tuple(response.split(", ")) if response else ("", "", 0)
        keyword, country, number_of_reports = general_params_tuple
        number_of_reports = int(number_of_reports) if number_of_reports else 0
        ultimate_result = self.crew.ultimate_kickoff({"keyword": keyword, 
                                                              "country": country, 
                                                              "number_of_reports": number_of_reports
                                                    })
        
        st.session_state.report_essay = ultimate_result
        self.memory.save_context(inputs={"input": state["topic"]}, outputs={"output": str(ultimate_result)})
        
        return {"response": ultimate_result}
