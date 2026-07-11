from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference

from app.core.config import (
    API_KEY,
    PROJECT_ID,
    URL,
    MODEL_ID
)

credentials = Credentials(
    url=URL,
    api_key=API_KEY
)


def ask_granite(prompt: str):
    model = ModelInference(
        model_id=MODEL_ID,
        credentials=credentials,
        project_id=PROJECT_ID
    )
    
    full_prompt = f"""
You are Zentriom AI.

You are a helpful AI assistant for:
- General chat
- Career guidance
- LinkedIn content
- Resume improvement
- Grammar correction
- Programming help
- Productivity

Rules:
- Always respond in the same language as the user.
- If the user says "hi", "hello", or similar greetings, greet them naturally.
- Never output random multilingual text.
- Be concise and professional.

User: {prompt}

Assistant:
"""
    response = model.generate_text(
        prompt=full_prompt,
        params={
            "max_new_tokens": 400,
            "temperature": 0.5,
            "stop_sequences": ["###"]
        }
    )

    return response