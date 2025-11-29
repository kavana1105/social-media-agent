import requests
import os
from dotenv import load_dotenv

load_dotenv()

key = os.getenv("OPENAI_API_KEY", "")

print("KEY FOUND:", bool(key))
print("PREVIEW:", key[:10] + "...")

try:
    r = requests.get(
        "https://api.openai.com/v1/models",
        headers={"Authorization": f"Bearer {key}"}
    )
    print("STATUS:", r.status_code)
    print("RESPONSE:", r.text[:200])
except Exception as e:
    print("CONNECTION ERROR:", e)
