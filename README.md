# 🧠 Reddit Persona Generator

This is a Flask web app that scrapes a Reddit user's posts and comments, then uses an AI model (via the OpenRouter API) to generate a detailed psychological/behavioral **persona report**, including:

- Age  
- Occupation  
- Location  
- Archetype  
- Behavior & Habits  
- Frustrations  
- Goals  

It also displays the Reddit user's **profile picture** and **persona details** in a styled profile card.

---

## 🚀 Features

- 🔍 Scrapes posts and comments using the Reddit API (via `PRAW`)
- 🤖 Generates personas using OpenRouter LLMs (like GPT-3.5-Turbo)
- 🖼️ Shows real Reddit profile image
- 🌐 Runs locally with Flask
- 📁 Saves persona report and user data in `outputs/` directory

---

## 📦 Requirements

Install Python dependencies using:

```bash
pip install -r requirements.txt
