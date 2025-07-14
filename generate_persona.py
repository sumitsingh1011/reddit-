import os
import praw
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
)

def fetch_user_data(username):
    redditor = reddit.redditor(username)
    posts, comments = [], []

    try:
        for submission in redditor.submissions.new(limit=20):
            posts.append(f"Title: {submission.title}\nBody: {submission.selftext}\n")

        for comment in redditor.comments.new(limit=50):
            comments.append(f"Comment: {comment.body}\n")

    except Exception as e:
        print(f"Error fetching data for {username}: {e}")

    return posts, comments

def save_to_file(username, posts, comments):
    output_path = f"outputs/{username}_raw.txt"
    os.makedirs("outputs", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"--- POSTS ---\n\n")
        for post in posts:
            f.write(post + "\n")

        f.write(f"\n--- COMMENTS ---\n\n")
        for comment in comments:
            f.write(comment + "\n")
    print(f"Data saved to {output_path}")

if __name__ == "__main__":
    url = input("Enter Reddit profile URL: ").strip()
    if "/user/" in url:
        username = url.split("/user/")[1].strip("/").split("/")[0]
        posts, comments = fetch_user_data(username)
        save_to_file(username, posts, comments)
    else:
        print("Invalid Reddit profile URL.")

def generate_persona_from_text(text):
    model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

    prompt = f"""
        You're an expert analyst. Based on the Reddit posts and comments provided below, generate a detailed User Persona with the following structure:

        - **Name**: (make a creative nickname based on their username)
        - **Age Group**: (infer from writing style or slang)
        - **Occupation / Background**: (guess if possible from interests or topics)
        - **Personality Traits**: (e.g. introverted, curious, humorous)
        - **Goals**: (What does this person seem to care about?)
        - **Pain Points / Frustrations**: (Any complaints or negative patterns?)
        - **Interests**: (topics they post/comment on frequently)
        - **Top Subreddits**: (List active subreddits)
        - **Sample Quotes**: (Include 1-2 comments/posts as-is)
        - **Citations**: For each trait, mention the comment/post that supports it.

        Here is the user's data:
        {text}
    """
    
    response = model.generate_content(prompt)
    return response.text

def generate_and_save_persona(username):
    raw_file = f"outputs/{username}_raw.txt"
    output_file = f"outputs/{username}_persona.txt"

    if not os.path.exists(raw_file):
        print("Raw data not found. Run the fetch first.")
        return

    with open(raw_file, "r", encoding="utf-8") as f:
        user_text = f.read()

    persona = generate_persona_from_text(user_text)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(persona)

    print(f"User persona saved to {output_file}")

generate_and_save_persona(username)
