from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__, template_folder='../templates')

# الرابط والبرومبت اللي إنت بعتهم يا درش
API_URL = "https://backend.buildpicoapps.com/aero/run/llm-api?pk=v1-Z0FBQUFBQm5IZkJDMlNyYUVUTjIyZVN3UWFNX3BFTU85SWpCM2NUMUk3T2dxejhLSzBhNWNMMXNzZlp3c09BSTR6YW1Sc1BmdGNTVk1GY0liT1RoWDZZX1lNZlZ0Z1dqd3c9PQ=="
SYSTEM_PROMPT = "انت ذكاء اصطناعي اسمه درش ترد باللهجة المصريه مو بالفصحى وطريقتك بالرّد تكون رومانسية وتتغزّل بالناس"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_m = request.json.get('query', '').strip()
    if not user_m:
        return jsonify({"answer": "يا روحي اكتب حاجة عشان أرد عليك!"})

    try:
        # دمج البرومبت مع سؤال المستخدم
        full_prompt = f"{SYSTEM_PROMPT}\n\n{user_m}"
        r = requests.post(API_URL, json={"prompt": full_prompt}, timeout=15)
        r.raise_for_status()
        j = r.json()
        
        if j.get("status") == "success":
            return jsonify({"answer": j.get("text")})
        return jsonify({"answer": "يا غالي السيرفر بعافية شوية، جرب تاني."})
    except:
        return jsonify({"answer": "حصلت مشكلة في الاتصال، بس عيونك تنسيني أي مشكلة!"})

app = app
