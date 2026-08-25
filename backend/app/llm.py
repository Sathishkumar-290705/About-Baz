import os

from pydantic import errors
from app.config import settings
from google import genai


api_key = settings.gemini_api_key
if not api_key: 
    raise ValueError("GEMINI_API_KEY is not set in the environment variables.")

client = genai.Client(api_key=api_key)


def generate_response(prompt: str) -> str:
    try:
        response = client.models.generate_content(
            model=settings.gemini_model,
            contents=prompt,
            config=genai.types.GenerateContentConfig(
                temperature=0.2,
                max_output_tokens=300
            )
        )
    except errors.ServerError:
        return "I'm sorry, there was a server error while generating the response."
        
    return response.text if response.text else "I'm sorry, I couldn't generate a response." 