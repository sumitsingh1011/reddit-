import os
import praw
from dotenv import load_dotenv

load_dotenv()

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
