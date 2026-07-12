from app.services.granite import ask_granite
from app.services.code_detector import detect_language

def explain_code(
    code: str,
):
    language = detect_language(code)
    
    prompt = f"""
    You are an expert software engineer.
    
    Explain this {language} code.

Code:
{code}

Rules:
- Explain step-by-step.
- Explain what each important section does.
- Explain functions, loops, conditions and variables.
- Keep explanations easy to understand.
- Use bullet points where helpful.
- Do not modify the code.
- Do not generate new code unless required for explanation.

    """
    explanation =ask_granite(prompt)
    
    return {
        "language": language,
        "explanation": explanation
    }