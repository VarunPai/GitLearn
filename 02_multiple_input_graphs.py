from typing import List, TypedDict
from langgraph.graph import StateGraph
from IPython.display import Image, display
import math

# Create Agent State
class AgentState(TypedDict):
    """Definition of the Agent"""
    values: List[int]
    name : str
    operation: str
    result : str

def process_values(state: AgentState) -> AgentState:
    """This function handles multiple different inputs"""
    if state["operation"] == "+":
        state["result"] = f"Hi, {state['name']}, Your sum = {sum(state['values'])}"
    elif state["operation"] == "*":
        state["result"] = f"Hi, {state['name']}, Your product = {math.prod(state['values'])}"
    else:
        state["result"] = "Invalid operation"

    return state


graph = StateGraph(AgentState)
graph.add_node("processor", process_values)
graph.set_entry_point("processor")
graph.set_finish_point("processor")

app = graph.compile()
display(Image(app.get_graph().draw_mermaid_png()))

result = app.invoke({"values":[1,2,3,4,5], "name": "Bob", "operation": "+"})
print(f"{result['result']}")

result = app.invoke({"values":[1,2,3,4,5], "name": "Bob", "operation": "*"})
print(f"{result['result']}")

result = app.invoke({"values":[1,2,3,4,5], "name": "Bob", "operation": "&"})
print(f"{result['result']}")
