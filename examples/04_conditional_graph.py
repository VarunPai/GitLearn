"""
Handle conditional nodes
"""
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from IPython.display import Image, display

# Create Agent State
class AgentState(TypedDict):
    """Definition of the Agent"""
    number1 : int
    operation1 : str
    number2 : int
    final_number1 : int

    number3: int
    operation2 : str
    number4: int
    final_number2 : int
    

def adder1(state: AgentState) -> AgentState:
    """This node adds two numbers"""
    state["final_number1"] = state["number1"] + state["number2"]
    return state

def subtractor1(state: AgentState) -> AgentState:
    """This node subtracts two numbers"""
    state["final_number1"] = state["number1"] - state["number2"]
    return state

def adder2(state: AgentState) -> AgentState:
    """This node adds two numbers"""
    state["final_number2"] = state["number3"] + state["number4"]
    return state

def subtractor2(state: AgentState) -> AgentState:
    """This node subtracts two numbers"""
    state["final_number2"] = state["number3"] - state["number4"]
    return state


def router1(state: AgentState) -> AgentState:
    """This node decides whether to add or subtract"""
    if state["operation1"] == "+":
        return "addition_operation"
    
    if state["operation1"] == "-":
        return "subtraction_operation"
    
def router2(state: AgentState) -> AgentState:
    """This node decides whether to add or subtract"""
    if state["operation2"] == "+":
        return "addition_operation"
    
    if state["operation2"] == "-":
        return "subtraction_operation"


graph = StateGraph(AgentState)
graph.add_node("adder1", adder1)
graph.add_node("subtractor1", subtractor1)
graph.add_node("router1", lambda state:state) # pass through function
graph.add_node("adder2", adder2)
graph.add_node("subtractor2", subtractor2)
graph.add_node("router2", lambda state:state) # pass through function

graph.add_edge(START, "router1")
graph.add_conditional_edges(
    "router1", 
    router1,
    {
        "addition_operation": "adder1",
        "subtraction_operation": "subtractor1"
    }
)

graph.add_edge("adder1", "router2")
graph.add_edge("subtractor1", "router2")
graph.add_conditional_edges(
    "router2", 
    router2,
    {
        "addition_operation": "adder2",
        "subtraction_operation": "subtractor2"
    }
)
graph.add_edge("adder2", END)
graph.add_edge("subtractor2", END)

app = graph.compile()
display(Image(app.get_graph().draw_mermaid_png()))

result = app.invoke({"number1":6, "number2":7, "operation1": "+", "number3": 6, "number4": 1, "operation2":"-"})
print(result["final_number1"], result["final_number2"])

result = app.invoke({"number1":65, "number2":32, "operation1": "-", "number3": 12, "number4": 14, "operation2":"+"})
print(result["final_number1"], result["final_number2"])

