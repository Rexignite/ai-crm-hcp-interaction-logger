import os
import re
from langgraph.graph import StateGraph, START, END
from langchain_groq import ChatGroq
from .state import AgentState
from .tools import *
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
print(f"GROQ_API_KEY loaded: {'Yes' if GROQ_API_KEY else 'No'}")

# ✅ MODEL CHANGE KAREIN - Ab llama-3.3-70b-versatile use karein
llm = ChatGroq(
    model="llama-3.3-70b-versatile",  # ✅ YEH CHANGE KIYA
    groq_api_key=GROQ_API_KEY,
    temperature=0.3
)

def classify_intent(state: AgentState):
    last_message = state['messages'][-1]['content'] if state['messages'] else ""
    msg = last_message.lower()
    
    if "log" in msg or "meeting" in msg or "met" in msg:
        intent = "log_interaction"
    elif "edit" in msg or "change" in msg or "update" in msg:
        intent = "edit_interaction"
    elif "search" in msg or "find" in msg:
        intent = "search_hcp"
    elif "follow" in msg or "reminder" in msg:
        intent = "schedule_followup"
    elif "summary" in msg or "summarize" in msg:
        intent = "generate_summary"
    else:
        intent = "unknown"
    
    return {"intent": intent}

def execute_tool(state: AgentState):
    intent = state['intent']
    last_message = state['messages'][-1]['content'] if state['messages'] else ""
    
    if intent == "log_interaction":
        result = log_interaction_tool(last_message, llm)
        return {"tool_output": result}
    elif intent == "edit_interaction":
        ids = re.findall(r'\d+', last_message)
        interaction_id = int(ids[0]) if ids else 1
        result = edit_interaction_tool(interaction_id, {"summary": last_message}, llm)
        return {"tool_output": result}
    elif intent == "search_hcp":
        query = re.sub(r'(search|find|for)', '', last_message).strip()
        result = search_hcp_tool(query)
        return {"tool_output": result}
    elif intent == "schedule_followup":
        ids = re.findall(r'\d+', last_message)
        interaction_id = int(ids[0]) if ids else 1
        result = schedule_followup_tool(interaction_id, 7)
        return {"tool_output": result}
    elif intent == "generate_summary":
        ids = re.findall(r'\d+', last_message)
        interaction_id = int(ids[0]) if ids else 1
        result = generate_summary_tool(interaction_id, llm)
        return {"tool_output": result}
    
    return {"tool_output": {"status": "error", "message": "Could not understand request"}}

def generate_response(state: AgentState):
    output = state.get('tool_output', {})
    response = output.get('message', output.get('summary', "I processed your request"))
    return {"messages": [{"role": "assistant", "content": response}]}

def create_agent():
    graph_builder = StateGraph(AgentState)
    
    graph_builder.add_node("classify", classify_intent)
    graph_builder.add_node("execute", execute_tool)
    graph_builder.add_node("respond", generate_response)
    
    graph_builder.add_edge(START, "classify")
    graph_builder.add_edge("classify", "execute")
    graph_builder.add_edge("execute", "respond")
    graph_builder.add_edge("respond", END)
    
    return graph_builder.compile()

agent = create_agent()