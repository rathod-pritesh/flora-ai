from ibm_watsonx_ai.foundation_models import ModelInference

from app.services.granite import ask_granite

def generate_linkedin_post(
    post_type: str,
    topic: str,
    experience: str,
    tone: str,
    length: str
):
    length_instruction = {
        "short": "Write 60-100 words.",
        "medium": "Write 120-180 words.",
        "long": "Write 200-300 words."
    }.get(length.lower(), "Write 120-180 words.")
    
    prompt = f"""
You are an expert LinkedIn caption writer.

Write a LinkedIn post that sounds like a real person.

Post Type:
{post_type}

Topic:
{topic}

Personal Experience:
{experience}

Tone:
{tone}

Length Requirement:
{length_instruction}

Rules:

- Write from perspective, not information.
- Use first person language.
- Focus on lessons, observations, mistakes, surprises, or mindset shifts.
- Do not explain the topic like an article.
- Do not sound like a marketing page.
- Do not sound like ChatGPT.
- Avoid corporate buzzwords.
- Avoid motivational clichés.
- Avoid phrases like:
  "excited to share"
  "thrilled"
  "game changer"
  "transformative journey"
  "hard work pays off"
  "grateful"

For CERTIFICATE posts:
- Focus more on what became clearer while learning.
- Focus less on the certificate itself.

For PROJECT posts:
- Focus on building process, debugging, mistakes, decisions.

For INTERNSHIP posts:
- Focus on real-world observations and learning.

For LEARNING posts:
- Focus on confusion becoming understanding.

Write naturally.

No headers.
No markdown.
No labels.

Maximum 220 words.

###
"""

    return ask_granite(prompt)