from flask import Flask, render_template, request
import os
import json

app = Flask(__name__)

# === Load user data and persona ===
def load_persona_data(username):
    try:
        with open(f"outputs/{username}_persona.txt", "r", encoding="utf-8") as f:
            persona = f.read()
        with open(f"outputs/{username}_data.json", "r", encoding="utf-8") as f:
            user_data = json.load(f)
        return persona, user_data
    except FileNotFoundError:
        return None, None

@app.route("/")
def index():
    return render_template("form.html")

@app.route("/result", methods=["POST"])
def result():
    username = request.form["username"]
    persona, user_data = load_persona_data(username)

    if persona and user_data:
        return render_template(
            "result.html",
            username=username,
            persona=persona,
            profile_img=user_data.get("profile_img")
        )
    else:
        return f"❌ Could not load data for user: {username}", 404

if __name__ == "__main__":
    app.run(debug=True, port=10000)
