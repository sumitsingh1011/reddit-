import requests
import os
from dotenv import load_dotenv

load_dotenv()

headers = {
    "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
}

response = requests.get("https://openrouter.ai/api/v1/models", headers=headers)

if response.status_code == 200:
    models = response.json().get("data", [])
    for model in models:
        print(f"{model['id']} → {model.get('name')}")
else:
    print("Failed to fetch models:", response.text)
