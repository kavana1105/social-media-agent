from dotenv import load_dotenv
import os
from agent_config import AGENT_INSTRUCTIONS
from vertexai.generative_models import GenerativeModel
from vertexai import init

load_dotenv()

PROJECT_ID = os.getenv("PROJECT_ID")
LOCATION = "us-central1"

def run_agent(user_input):
    init(project=PROJECT_ID, location=LOCATION)

    model = GenerativeModel("gemini-1.5-flash")

    full_prompt = f"{AGENT_INSTRUCTIONS}\nUser request: {user_input}"

    response = model.generate_content(full_prompt)
    return response.text

if __name__ == "__main__":
    print("✨ Social Media Agent Ready! ✨")

    while True:
        text = input("\nYou: ")
        output = run_agent(text)
        print("\nAgent:", output)
