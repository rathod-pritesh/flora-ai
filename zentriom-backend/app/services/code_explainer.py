from app.services.granite import ask_granite
from app.services.code_detector import detect_language

def explain_code(
    code: str,
):
    language = detect_language(code)
    
    prompt = f"""
    You are a senior software engineer.

Task:
Explain the following {language} code in a concise and beginner-friendly way.

Code:
{code}

Rules:
- Start directly with the explanation.
- Do NOT repeat the original code.
- Do NOT write "Code:" or "Explanation:".
- Do NOT write introductions like "Certainly!".
- Do NOT write summaries at the end.
- Keep the response concise and focused.
- Explain only what exists in the code.
- Use markdown bullet points.
- Explain variables, functions, loops, conditions, and important operations if present.
- If the code is short, keep the explanation short.
- If the code contains no loops or conditions, do not mention them.
- Use this format:

• Purpose:
  One sentence describing what the code does.

• Breakdown:
  - First important part
  - Second important part
  - Third important part

• Output:
  Describe the expected result.

Return only the explanation.

    """
    explanation =ask_granite(prompt)
    
    return {
        "language": language,
        "explanation": explanation
    }