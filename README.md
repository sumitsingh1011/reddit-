# Reddit Persona Generator

A Python script that scrapes a Reddit user's posts and comments and uses **Gemini Pro (LLM)** to generate a detailed **User Persona**, including citations of which post or comment led to each trait.

---

## Features

- Input: Reddit user profile URL
- Scrapes latest posts and comments from the user
- Uses Gemini Pro (Google's LLM) to analyze behavior
- Outputs a structured User Persona in `.txt` format
- Cites which post or comment supports each trait
- Follows PEP-8 coding guidelines

---

## Tech Stack

- Python 3
- PRAW (Reddit API Wrapper)
- Google Generative AI (Gemini Pro)
- dotenv (`.env` file for API keys)

---

## Setup Instructions

### 1. Clone this repository

```bash
git clone https://github.com/tusharharyana/reddit-persona-generator.git
cd reddit-persona-generator
```

### 2. (Optional) Create a virtual environment
```bash
python -m venv venv
venv\Scripts\activate
```
### 3. Install the dependencies
```bash
pip install -r requirements.txt
```

### 4. Create a .env file
```bash
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
REDDIT_USER_AGENT=your_user_agent_string
GEMINI_API_KEY=your_gemini_api_key
```

## How to Use

Run the script and enter a Reddit profile URL:
```bash
python generate_persona.py
```

Example input : `https://www.reddit.com/user/kojied/`

## LLM Prompt (Used with Gemini Pro)
The LLM prompt was designed to return structured personas and include references to specific posts/comments used for inference.
