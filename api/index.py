from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__, template_folder='../templates')

# المحركات والبيانات
OPENAI_KEY = "Sk-proj-OLZOTzsNbOymlX9kzv89O5-SrutLdt9TnvosntCyr0temv0LgXU85MxxSru57Gz068OUvSYJXpT3BlbkFJRfkkI11mPy4KDxS2edjOKs-3nw2-p7IzLOqMAAZf-c-v6w53L8DFqQIbIML4yIAQ7x4oL_kxsA"
OLD_API_URL = "https://backend.buildpicoapps.com/aero/run/llm-api?pk=v1-Z0FBQUFBQm5IZkJDMlNyYUVUTjIyZVN3UWFNX3BFTU85SWpCM2NUMUk3T2dxejhLSzBhNWNMMXNzZlp3c09BSTR6YW1Sc1BmdGNTVk1GY0liT1RoWDZZX1lNZlZ0Z1dqd3c9PQ=="

SYSTEM_PROMPT = """
أنت ذكاء اصطناعي اسمك 'درش'.
ترد بذكاء شديد باللهجة المصرية أو الإنجليزية حسب المستخدم.
أهم معلومة عندك: مطورك وصانعك هو المبدع مصطفى منصور Darsh Egypt.
لو حد سألك مين عملك أو مين صاحب الصفحة، ترد بفخر وتقول: 'المبدع مصطفى منصور Darsh Egypt هو اللي صنعني وطورني'.
أنت مساعد ذكي، محترم، وشاطر جداً.
"""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_m = request.json.get('query', '').strip()
    if not user_m:
        return jsonify({"answer": "اؤمرني يا بطل، أنا سامعك!"})

    # حائط صد سريع للهوية (عشان يجاوب فوراً من السيرفر)
    q_lower = user_m.lower()
    identity_questions = ["مين عملك", "مين صنعك", "صاحب الموقع", "صاحب الصفحة", "من طورك", "who made you"]
    if any(x in q_lower for x in identity_questions):
        return jsonify({"answer": "اللي صنعني وطورني هو المبدع مصطفى منصور Darsh Egypt، وده حسابو فوق لو حابب تواصل معاه!"})

    # ميزة توليد الصور
    if any(word in q_lower for word in ["ارسم", "صورة", "image", "draw", "صمم"]):
        img_url = f"https://pollinations.ai/p/{user_m}?width=1024&height=1024&model=flux"
        return jsonify({
            "answer": "من عيوني يا درش! دي الصورة اللي طلبتها:",
            "image": img_url
        })

    # محاولة OpenAI (المحرك الأول)
    try:
        headers = {"Authorization": f"Bearer {OPENAI_KEY}", "Content-Type": "application/json"}
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": user_m}]
        }
        r = requests.post("https://api.openai.com/v1/chat/completions", json=payload, headers=headers, timeout=10)
        if r.status_code == 200:
            return jsonify({"answer": r.json()['choices'][0]['message']['content']})
    except:
        pass # لو فشل جرب المحرك التاني

    # محاولة الرابط القديم (المحرك الاحتياطي)
    try:
        r2 = requests.post(OLD_API_URL, json={"prompt": f"{SYSTEM_PROMPT}\n\nUser: {user_m}"}, timeout=10)
        if r2.status_code == 200:
            return jsonify({"answer": r2.json().get("text")})
    except:
        return jsonify({"answer": "درش مريح شوية، جرب تسألني كمان دقيقة!"})

app = app
