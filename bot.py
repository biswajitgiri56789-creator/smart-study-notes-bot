import os
import json
import random
import requests
from datetime import datetime
import pytz

# ===============================
# ENV (DO NOT CHANGE)
# ===============================
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
TIMEZONE = os.getenv("TIMEZONE", "Asia/Kolkata")

API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

# ===============================
# DATA FILES
# ===============================
DATA_FILES = {
    "Class 11": "data_class11.json",
    "Class 12": "data_class12.json",
    "College First Year": "data_college_year1.json",
    "College Second Year": "data_college_year2.json",
    "College Third Year": "data_college_year3.json",
}

POSTED_FILE = "posted_questions.json"

BANGLA_SUBJECTS = {
    "Political Science",
    "History",
    "Geography",
    "Economics",
    "Business Studies",
    "Accountancy"
}

# ===============================
# HELPERS
# ===============================
def is_bangla(subject):
    return subject in BANGLA_SUBJECTS

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_posted():
    if not os.path.exists(POSTED_FILE):
        return set()
    with open(POSTED_FILE, "r", encoding="utf-8") as f:
        return set(json.load(f))

def save_posted(posted):
    with open(POSTED_FILE, "w", encoding="utf-8") as f:
        json.dump(list(posted), f, ensure_ascii=False, indent=2)

def make_question(concept, chapter, subject):
    if is_bangla(subject):
        return random.choice([
            f"{concept} কী? ব্যাখ্যা করো।",
            f"{chapter} অধ্যায়ের আলোকে {concept} আলোচনা করো।",
            f"{concept} কেন গুরুত্বপূর্ণ?",
            f"{concept} বিস্তারিতভাবে লেখো।"
        ])
    else:
        return random.choice([
            f"What is {concept}? Explain.",
            f"Discuss {concept} with reference to {chapter}.",
            f"Why is {concept} important?",
            f"Describe {concept} in detail."
        ])

# ===============================
# BUILD MESSAGE
# ===============================
def build_message():
    posted = load_posted()

    msg = (
        "📘 *Smart Study Notes*\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "🎯 *Exam Important Questions*\n\n"
    )

    for class_name, file in DATA_FILES.items():
        data = load_json(file)
        msg += f"📚 *{class_name}*\n\n"

        for item in data:
            subject = item["subject"]
            chapter = item["chapter"]
            importance = item["importance"]
            exam = item["tag"]

            concept = random.choice(item["concepts"])
            question = make_question(concept, chapter, subject)

            key = f"{class_name}|{subject}|{chapter}|{question}"
            if key in posted:
                continue

            posted.add(key)

            label = "প্রশ্ন" if is_bangla(subject) else "Question"

            msg += (
                f"📖 *Subject:* {subject}\n"
                f"🧩 *Chapter:* {chapter}\n"
                f"❓ *{label}:* {question}\n"
                f"🟢 *Importance:* {importance}\n"
                f"🏷️ *Exam:* {exam}\n"
                "━━━━━━━━━━━━━━━━━━\n"
            )

    save_posted(posted)

    msg += (
        "📌 Follow & Share: @smartstudynotes11\n"
        "#ExamSuggestion #SmartStudy"
    )

    return msg

# ===============================
# SEND
# ===============================
def send_message(text):
    requests.post(API_URL, data={
        "chat_id": CHANNEL_ID,
        "text": text,
        "parse_mode": "Markdown"
    })

# ===============================
# MAIN
# ===============================
def main():
    tz = pytz.timezone(TIMEZONE)
    _ = datetime.now(tz)

    message = build_message()
    if message.strip():
        send_message(message)

if __name__ == "__main__":
    main()
