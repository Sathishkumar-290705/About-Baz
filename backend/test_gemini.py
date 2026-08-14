from google import genai
from dotenv import load_dotenv
import os
from app.config import settings



api_key = settings.gemini_api_key
if not api_key:
    raise ValueError("GEMINI_API_KEY is not set in the environment variables.")


client = genai.Client(api_key=api_key)

interaction = client.interactions.create(
    model="gemini-3.6-flash",
    input="my name is sathish and i am a software engineer. I want to learn about the latest advancements in AI and how they can be applied to real-world problems. Can you provide me with some insights and resources to get started?"
)

print(interaction.output_text)