from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import requests
import google.auth
from google.auth.transport.requests import Request
from google.oauth2 import service_account
import json

app = FastAPI()

# Load credentials from JSON file
CREDENTIALS_FILE = r"YOUR_KEY"  # replace with your file path
API_URL = "https://language.googleapis.com/v1/documents:analyzeSentiment"

# Authenticate and get access token
def get_access_token():
    credentials = service_account.Credentials.from_service_account_file(
        CREDENTIALS_FILE,
        scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )
    auth_req = Request()
    credentials.refresh(auth_req)
    return credentials.token

# Function for sentiment analysis
def analyze_emotion(text: str) -> str:
    headers = {
        "Authorization": f"Bearer {get_access_token()}",
        "Content-Type": "application/json"
    }
    data = {
        "document": {"type": "PLAIN_TEXT", "content": text},
        "encodingType": "UTF8"
    }
    response = requests.post(API_URL, json=data, headers=headers)
    sentiment = response.json().get("documentSentiment", {})
    score = sentiment.get("score", 0)
    magnitude = sentiment.get("magnitude", 0)

    # Interpretation of mental state based on score and magnitude
    if score < -0.6 and magnitude > 5:
        return "High likelihood of anxiety or emotional distress."
    elif score < -0.3 and magnitude < 5:
        return "Possible signs of depression or low mood."
    elif score > 0.3 and magnitude > 5:
        return "Positive sentiment, but high emotional sensitivity detected."
    elif score == 0 and magnitude > 5:
        return "Neutral sentiment with high emotional intensity; potential mixed feelings."
    else:
        return "Stable sentiment detected; no strong indications of mental health issues."

# Main page with form
@app.get("/", response_class=HTMLResponse)
async def form_post():
    with open("app/templates/index.html", "r", encoding="utf-8") as file:
        return file.read()

# Results page
@app.post("/", response_class=HTMLResponse)
async def form_submit(
    question1: str = Form(...),
    question2: str = Form(...),
    question3: str = Form(...),
    question4: str = Form(...),
    question5: str = Form(...),
    question6: str = Form(...),
    question7: str = Form(...),
    question8: str = Form(...),
    question9: str = Form(...),
    question10: str = Form(...)
):
    # Combine questions and answers for better context
    questions = [
        "How often do you feel anxious?", "Do you find it difficult to focus on tasks?",
        "Do you often feel overwhelmed by stress?", "Do you experience sleep disturbances?",
        "Have you lost interest in activities you once enjoyed?", "Do you feel disconnected from others?",
        "Are you experiencing feelings of hopelessness?", "Do you have trouble making decisions?",
        "Have you been feeling sad or depressed recently?", "Do you often experience mood swings?"
    ]
    answers = [
        question1, question2, question3, question4, question5,
        question6, question7, question8, question9, question10
    ]
    
    # Formulate combined text for sentiment analysis
    combined_text = " ".join([f"{q} {a}" for q, a in zip(questions, answers)])

    # Analyze emotion based on combined text
    mental_state = analyze_emotion(combined_text)

    # Read HTML result page and replace placeholder with prediction
    with open("app/templates/result.html", "r", encoding="utf-8") as file:
        result_page = file.read()

    result_page = result_page.replace("{{ prediction }}", mental_state)

    return result_page
