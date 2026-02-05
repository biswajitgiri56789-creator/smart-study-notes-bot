import os
import json
import random
import requests

# =======================
# ENV (GitHub Secrets)
# =======================
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
TIMEZONE = os.getenv("TIMEZONE", "Asia/Kolkata")

if not BOT_TOKEN or not CHANNEL_ID:
    raise ValueError("BOT_TOKEN or CHANNEL_ID is missing in GitHub Secrets")

# =======================
# DATA FILES
# =======================
FILES = [
    "data_class11.json",
    "data_class12.json",
    "data_college_year1.json",
    "data_college_year2.json",
    "data_college_year3.json"
]

POSTED_FILE = "posted_questions.json"

# =======================
# HELPERS
# =======================
def load_json(path, default):
    if not os.path.exists(path):
        return default
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# =======================
# LOAD POSTED HISTORY
# =======================
posted = load_json(POSTED_FILE, {"posted": []})

message = (
    "📘 *Smart Study Notes*\n"
    "━━━━━━━━━━━━━━━━━━\n"
    "🎯 *Exam Important Question (Suggestion)*\n\n"
)

added_any = False

# =======================
# PICK QUESTIONS
# =======================
for file in FILES:
    data = load_json(file, [])

    if not data:
        continue

    item = random.choice(data)

    template = random.choice(item.get("templates", []))
    concept = random.choice(item.get("concepts", []))
    question = template.replace("{{concept}}", concept)

    key = f"{item.get('class')}-{item.get('subject')}-{question}"

    if key in posted["posted"]:
        continue

    posted["posted"].append(key)
    added_any = True

    message += (
        f"📚 *Class:* {item.get('class')}\n"
        f"📖 *Subject:* {item.get('subject')}\n"
        f"🧩 *Chapter:* {item.get('chapter')}\n\n"
        f"❓ *Question:*\n{question}\n\n"
        f"🟢 *Importance:* {item.get('importance')}\n"
        f"🏷️ *Type:* {item.get('tag')}\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
    )

# =======================
# SEND TO TELEGRAM
# =======================
if added_any:
    message += (
        "📌 *Follow & Share:* @smartstudynotes11\n"
        "#ExamSuggestion #StudyNotes"
    )

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHANNEL_ID,
        "text": message,
        "parse_mode": "Markdown"
    }

    response = requests.post(url, json=payload, timeout=20)

    if response.status_code != 200:
        raise RuntimeError(f"Telegram API error: {response.text}")

    save_json(POSTED_FILE, posted)
