"""
Handle looping nodes
"""
from typing import List, TypedDict
from langgraph.graph import StateGraph, START, END
from IPython.display import Image, display
import random

# Create Agent State
class AgentState(TypedDict):
    """Definition of the Agent"""
    name : str
    number: int
    guesses : List[int]
    attempts : int
    lower_bound : int
    upper_bound : int
    

def setup_node(state: AgentState) -> AgentState:
    """This is a setup node. Creates greeting and number"""
    state["name"] = f"Hi, there {state['name']}"
    state["lower_bound"] = 1
    state["upper_bound"] = 20
    state["number"] = random.randint(state["lower_bound"], state["upper_bound"])
    state["guesses"] = []
    state["attempts"] = 0
    return state

def guess_node(state: AgentState) -> AgentState:
    """This node guesses a number"""
    possible_guesses = [i for i in range(state["lower_bound"], state["upper_bound"] + 1) if i not in state["guesses"]]
    if possible_guesses:
        guess = random.choice(possible_guesses)
    else:
        guess = random.randint(state["lower_bound"], state["upper_bound"])
    
    state["guesses"].append(guess)
    state["attempts"] += 1
    print(f"Attempt {state['attempts']}: Guessing {guess} (Current range: {state['lower_bound']}-{state['upper_bound']})")
    return state


def hint_node(state: AgentState) -> AgentState:
    """This node provides hint based on the number"""
    last_guess = state["guesses"][-1]
    target_number = state["number"]

    if last_guess < target_number:
        state["hint"] = f"The number {last_guess} is too low. Try higher!"
        state["lower_bound"] = max(state["lower_bound"], last_guess + 1)
        print(f"Hint: {state['hint']}")
        
    elif last_guess > target_number:
        state["hint"] = f"The number {last_guess} is too high. Try lower!"
      
        state["upper_bound"] = min(state["upper_bound"], last_guess - 1)
        print(f"Hint: {state['hint']}")
    else:
        state["hint"] = f"Correct! You found the number {target_number} in {state['attempts']} attempts."
        print(f"Success! {state['hint']}")
    
    return state

def should_condition(state: AgentState) -> AgentState:
    """Determine if we should continue guessing or end the game"""
    
    # There are 2 end conditions - either 7 is reached or the correct number is guessed
    
    latest_guess = state["guesses"][-1]
    if latest_guess == state["number"]:
        print(f"GAME OVER: Number found!")
        return "end"
    elif state["attempts"] >= 7:
        print(f"GAME OVER: Maximum attempts reached! The number was {state['number']}")
        return "end"
    else:
        print(f"CONTINUING: {state['attempts']}/7 attempts used")
        return "continue"


graph = StateGraph(AgentState)
graph.add_node("setup", setup_node)
graph.add_node("guess", guess_node)
graph.add_node("hint_node", hint_node)


graph.add_edge(START, "setup")
graph.add_edge("setup", "guess")
graph.add_edge("guess", "hint_node")
graph.add_conditional_edges(
    "hint_node",
    should_condition,
    {
        "end": END,
        "continue": "guess"
    }
)

app = graph.compile()
display(Image(app.get_graph().draw_mermaid_png()))

result = app.invoke({"name": "Sam"})
print(result["number"])



