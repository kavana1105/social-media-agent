from dotenv import load_dotenv
import os

load_dotenv()  # this loads variables from .env

key = os.getenv("OPENAI_API_KEY", "")

print("KEY FOUND:", bool(key))
print("STARTS WITH sk- or sk-proj-:", key.startswith("sk-") or key.startswith("sk-proj-"))
print("PREVIEW:", key[:10] + "...")