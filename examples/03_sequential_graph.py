"""
Handle multiple nodes
"""
from typing import List, TypedDict
from langgraph.graph import StateGraph
from IPython.display import Image, display
import math

# Create Agent State
class AgentState(TypedDict):
    """Definition of the Agent"""
    name : str
    age: str
    skills: List[str]
    final : str

def first_node(state: AgentState) -> AgentState:
    """This is the first node of the sequence"""
    state['final'] = f"{state['name']}, welcome to the system!"
    return state

def second_node(state: AgentState) -> AgentState:
    """This is the second node of the sequence"""
    state['final'] = state['final'] + f"You are {state['age']} years old!"
    return state

def third_node(state: AgentState) -> AgentState:
    """This is the third node of the sequence"""
    state['final'] = state['final'] + f"You have skills in {','.join(state['skills'])}"
    return state


graph = StateGraph(AgentState)
graph.add_node("first_node", first_node)
graph.add_node("second_node", second_node)
graph.add_node("third_node", third_node)

graph.set_entry_point("first_node")
graph.add_edge("first_node", "second_node")
graph.add_edge("second_node", "third_node")
graph.set_finish_point("third_node")

app = graph.compile()
display(Image(app.get_graph().draw_mermaid_png()))

result = app.invoke({"name":"Bob", "age":"22", "skills":["Python", "C++"]})
print(result["final"])

