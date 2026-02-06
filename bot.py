import os
import json
import random
import requests
from datetime import datetime
import pytz

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
TIMEZONE = os.getenv("TIMEZONE", "Asia/Kolkata")

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
    "Political Science", "History", "Geography",
    "Economics", "Business Studies", "Accountancy"
]

# ---------- Helpers ----------

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def detect_lang(subject):
    return "bn" if subject in BANGLA_SUBJECTS else "en"

def today_date():
    tz = pytz.timezone(TIMEZONE)
    return datetime.now(tz).strftime("%Y-%m-%d")

def auto_reset():
    data = load_json(POSTED_FILE)
    if data["date"] != today_date():
        data["date"] = today_date()
        data["posted"] = []
        save_json(POSTED_FILE, data)
    return data

def ai_generate_question(concept, chapter, subject):
    bn = detect_lang(subject) == "bn"
    if bn:
        return random.choice([
            f"{concept} কী? ব্যাখ্যা করো।",
            f"{chapter} অধ্যায়ের আলোকে {concept} আলোচনা করো।",
            f"{concept} কেন গুরুত্বপূর্ণ?",
            f"{concept} সংক্ষেপে লেখো।"
        ])
    else:
        return random.choice([
            f"What is {concept}? Explain.",
            f"Discuss {concept} with reference to {chapter}.",
            f"Why is {concept} important?",
            f"Write short notes on {concept}."
        ])

# ---------- Main Logic ----------

def build_message():
    posted_data = auto_reset()
    posted = set(posted_data["posted"])

    msg = (
        "📘 *Smart Study Notes*\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "🎯 *Exam Important Questions (Suggestion)*\n\n"
    )

    new_added = False

    for class_name, file in DATA_FILES.items():
        data = load_json(file)
        msg += f"📚 *{class_name}*\n\n"

        for item in data:
            subject = item["subject"]
            chapter = item["chapter"]
            importance = item.get("importance", "High")
            tag = item.get("tag", "Exam")

            concept = random.choice(item["concepts"])
            question = ai_generate_question(concept, chapter, subject)

            key = f"{class_name}|{subject}|{chapter}|{question}"
            if key in posted:
                continue

            posted.add(key)
            new_added = True

            q_label = "প্রশ্ন" if detect_lang(subject) == "bn" else "Question"

            msg += (
                f"📖 Subject: {subject}\n"
                f"🧩 Chapter: {chapter}\n"
                f"❓ {q_label}: {question}\n"
                f"🟢 Importance: {importance}\n"
                f"🏷️ Type: {tag}\n"
                "━━━━━━━━━━━━━━━━━━\n"
            )

    if not new_added:
        return None

    posted_data["posted"] = list(posted)
    save_json(POSTED_FILE, posted_data)

    msg += "\n📌 Follow & Share: @smartstudynotes11\n#SmartStudy #ExamSuggestion"
    return msg

def send_message(text):
    requests.post(API_URL, data={
        "chat_id": CHANNEL_ID,
        "text": text,
        "parse_mode": "Markdown"
    })

def main():
    msg = build_message()
    if msg:
        send_message(msg)

if __name__ == "__main__":
    main()
