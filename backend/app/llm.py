import os 

from app.config import settings
from google import genai


api_key = settings.gemini_api_key
if not api_key: 
    raise ValueError("GEMINI_API_KEY is not set in the environment variables.")
client = genai.Client(api_key=api_key)


def generate_response(prompt: str) -> str:
    interaction = client.interactions.create(
        model=settings.gemini_model,
        input=prompt
    )

    return interaction.output_text