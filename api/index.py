from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__, template_folder='../templates')

API_URL = "https://backend.buildpicoapps.com/aero/run/llm-api?pk=v1-Z0FBQUFBQm5IZkJDMlNyYUVUTjIyZVN3UWFNX3BFTU85SWpCM2NUMUk3T2dxejhLSzBhNWNMMXNzZlp3c09BSTR6YW1Sc1BmdGNTVk1GY0liT1RoWDZZX1lNZlZ0Z1dqd3c9PQ=="

SYSTEM_PROMPT = """
أنت ذكاء اصطناعي ذكي جداً اسمك 'درش'.
تجيد التحدث بكل اللغات (مصري، إنجليزي، فصحى).
صاحب الصفحة ومطورك هو المبدع مصطفى منصور Darsh Egypt.
أجب بذكاء ولباقة واحترافية.
"""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_m = request.json.get('query', '').strip()
    if not user_m:
        return jsonify({"answer": "أنا سامعك، اتفضل اسأل!"})

    q = user_m.lower()
    if any(x in q for x in ["صاحب", "عملك", "مطورت", "من انت"]):
        return jsonify({"answer": "أنا درش، ذكاء اصطناعي طورني المبدع مصطفى منصور Darsh Egypt."})

    try:
        full_prompt = f"{SYSTEM_PROMPT}\n\nUser: {user_m}"
        r = requests.post(API_URL, json={"prompt": full_prompt}, timeout=15)
        r.raise_for_status()
        j = r.json()
        if j.get("status") == "success":
            return jsonify({"answer": j.get("text")})
        return jsonify({"answer": "السيرفر مشغول، حاول تاني يا بطل."})
    except:
        return jsonify({"answer": "حصل خطأ في الاتصال، أنا معاك دايماً."})

app = app
