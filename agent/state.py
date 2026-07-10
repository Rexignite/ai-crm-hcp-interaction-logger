from typing import TypedDict, List, Dict, Any

class AgentState(TypedDict):
    messages: List[Dict[str, str]]
    intent: str
    tool_output: Dict[str, Any]
    extracted_data: Dict[str, Any]
    interaction_id: int