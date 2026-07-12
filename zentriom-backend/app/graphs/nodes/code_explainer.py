from app.services.code_explainer import explain_code

def code_explainer_node(state):
    
    result = explain_code(
        state["code"]
    )
    
    return {
        "result": result["explanation"],
        "language": result["language"]
    }