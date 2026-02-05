import json, random, requests

BOT_TOKEN = "এখানে_তোমার_BOT_TOKEN_পেস্ট_করো"
CHANNEL_ID = "@smartstudynotes11"

FILES = [
    "data_class11.json",
    "data_class12.json",
    "data_college_year1.json",
    "data_college_year2.json",
    "data_college_year3.json"
]

def load(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

posted = load("posted_questions.json")
message = "📘 *Smart Study Notes*\n━━━━━━━━━━━━━━━━━━\n🎯 *Exam Important Question (Suggestion)*\n\n"
added = False

for file in FILES:
    data = load(file)
    item = random.choice(data)
    template = random.choice(item["templates"])
    concept = random.choice(item["concepts"])
    question = template.replace("{{concept}}", concept)

    key = f"{item['class']}-{item['subject']}-{question}"

    if key not in posted["posted"]:
        posted["posted"].append(key)
        added = True

        message += f"""
📚 *Class:* {item['class']}
📖 *Subject:* {item['subject']}
🧩 *Chapter:* {item['chapter']}

❓ *Question:*
{question}

🟢 *Importance:* {item['importance']}
🏷️ *Type:* {item['tag']}

━━━━━━━━━━━━━━━━━━
"""

if not added:
    posted["posted"] = []

message += "📌 Follow & Share: @smartstudynotes11\n#ExamSuggestion #StudyNotes"

requests.post(
    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
    data={"chat_id": CHANNEL_ID, "text": message, "parse_mode": "Markdown"}
)

save("posted_questions.json", posted)