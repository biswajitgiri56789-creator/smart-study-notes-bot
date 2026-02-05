import os
import json
import random
from datetime import datetime
import pytz
import requests

# ===============================
# ENV VARIABLES (DO NOT TOUCH)
# ===============================
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
TIMEZONE = os.getenv("TIMEZONE", "Asia/Kolkata")

# ===============================
# CONSTANTS
# ===============================
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

DATA_FILES = {
    "Class 11": "data_class11.json",
    "Class 12": "data_class12.json",
    "College First Year": "data_college_year1.json",
    "College Second Year": "data_college_year2.json",
    "College Third Year": "data_college_year3.json"
}

POSTED_FILE = "posted_questions.json"

BANGLA_SUBJECTS = [
    "Political Science",
    "History",
    "Geography",
    "Economics",
    "Business Studies",
    "Accountancy"
]

# ===============================
# UTILITY FUNCTIONS
# ===============================
def detect_language(subject):
    return "bn" if subject in BANGLA_SUBJECTS else "en"


def load_json(file):
    with open(file, "r", encoding="utf-8") as f:
        return json.load(f)


def load_posted():
    if not os.path.exists(POSTED_FILE):
        return set()
    with open(POSTED_FILE, "r", encoding="utf-8") as f:
        return set(json.load(f))


def save_posted(posted):
    with open(POSTED_FILE, "w", encoding="utf-8") as f:
        json.dump(list(posted), f, ensure_ascii=False, indent=2)


def generate_question(concept, subject, chapter):
    lang = detect_language(subject)

    if lang == "bn":
        return random.choice([
            f"{concept} কী? ব্যাখ্যা করো।",
            f"{chapter} অধ্যায়ের আলোকে {concept} আলোচনা করো।",
            f"{concept} কেন গুরুত্বপূর্ণ?",
            f"{concept} বিস্তারিতভাবে বর্ণনা করো।"
        ])
    else:
        return random.choice([
            f"What is {concept}? Explain.",
            f"Discuss {concept} with reference to {chapter}.",
            f"Why is {concept} important?",
            f"Describe {concept} in detail."
        ])


# ===============================
# MAIN LOGIC
# ===============================
def build_message():
    posted = load_posted()

    message = (
        "📘 Smart Study Notes\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "🎯 Exam Important Questions (Suggestion)\n\n"
    )

    for class_name, file_name in DATA_FILES.items():
        data = load_json(file_name)
        message += f"📚 **{class_name}**\n\n"

        for item in data:
            subject = item["subject"]
            chapter = item["chapter"]
            importance = item["importance"]
            tag = item["tag"]

            concept = random.choice(item["concepts"])
            question = generate_question(concept, subject, chapter)

            unique_key = f"{class_name}|{subject}|{chapter}|{question}"
            if unique_key in posted:
                continue

            posted.add(unique_key)

            label = "প্রশ্ন" if detect_language(subject) == "bn" else "Question"

            message += (
                f"📖 Subject: {subject}\n"
                f"🧩 Chapter: {chapter}\n"
                f"❓ {label}: {question}\n"
                f"🟢 Importance: {importance}\n"
                f"🏷️ Exam Type: {tag}\n"
                "━━━━━━━━━━━━━━━━━━\n"
            )

    save_posted(posted)

    message += (
        "📌 Follow & Share: @smartstudynotes11\n"
        "#ExamSuggestion #SmartStudy"
    )

    return message


def send_to_telegram(text):
    payload = {
        "chat_id": CHANNEL_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    requests.post(API_URL, data=payload)


# ===============================
# ENTRY POINT
# ===============================
def main():
    tz = pytz.timezone(TIMEZONE)
    now = datetime.now(tz)

    message = build_message()
    send_to_telegram(message)


if __name__ == "__main__":
    main()
