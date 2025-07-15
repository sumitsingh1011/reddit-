import os
import json
import re
import praw
from dotenv import load_dotenv

load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
)

def extract_username(input_str):
    match = re.search(r"(?:u/|user/)?([A-Za-z0-9_-]+)", input_str.strip())
    if match:
        return match.group(1)
    else:
        print("❌ Invalid Reddit username or URL.")
        return None

def fetch_user_data(username, limit=50):
    redditor = reddit.redditor(username)
    data = {
        "username": username,
        "profile_img": getattr(redditor, "icon_img", None),
        "description": getattr(redditor.subreddit, "public_description", "") if hasattr(redditor, "subreddit") else "",
        "total_karma": redditor.link_karma + redditor.comment_karma,
        "posts": [],
        "comments": []
    }

    for submission in redditor.submissions.new(limit=limit):
        data["posts"].append({
            "title": submission.title,
            "selftext": submission.selftext,
            "subreddit": str(submission.subreddit)
        })

    for comment in redditor.comments.new(limit=limit):
        data["comments"].append({
            "body": comment.body,
            "subreddit": str(comment.subreddit)
        })

    return data

def generate_persona_openrouter(user_data):
    import requests

    prompt = f"""Based on the following Reddit activity, create a persona:

    Posts:
    {user_data['posts']}

    Comments:
    {user_data['comments']}

    Format:
    - Age
    - Occupation
    - Location
    - Archetype
    - Behaviour & Habits
    - Frustrations
    - Goals
    """

    headers = {
        "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
        "HTTP-Referer": "http://localhost",
        "X-Title": "RedditPersonaBuilder"
    }

    payload = {
        "model": "openai/gpt-3.5-turbo-16k",  # Make sure model is supported
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        print("❌ OpenRouter API Error:", response.status_code, response.text)
        return None

def save_persona_output(persona, username, user_data):
    os.makedirs("outputs", exist_ok=True)

    with open(f"outputs/{username}_persona.txt", "w", encoding="utf-8") as f:
        f.write(persona)

    with open(f"outputs/{username}_data.json", "w", encoding="utf-8") as f:
        json.dump(user_data, f, indent=2)
