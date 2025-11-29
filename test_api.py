from dotenv import load_dotenv
import os
from openai import OpenAI

# Force load the correct .env file by giving the full path
load_dotenv(dotenv_path=r"C:\Users\Kavana B H\Desktop\social media agent\.env")

key = os.getenv("OPENAI_API_KEY")

print("KEY FOUND:", bool(key))
print("PREVIEW:", key[:10] + "...")

client = OpenAI(api_key=key)

try:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Hello, can you confirm my API key works?"}]
    )
    print("API CALL SUCCESS ✅")
    print("Response:", response.choices[0].message.content)
except Exception as e:
    print("API CALL FAILED ❌")
    print("Error:", e)