from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__, template_folder='../templates')

SYSTEM_PROMPT = "أنت 'درش'، ذكاء اصطناعي مطوره مصطفى منصور. رد دايماً بالمصري وخليك ذكي وسريع."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    user_m = data.get('query', '').strip()
    image_data = data.get('image')

    # توليد الصور
    if any(word in user_m.lower() for word in ["ارسم", "صورة", "image"]):
        img_url = f"https://pollinations.ai/p/{user_m}?width=1024&height=1024&model=flux"
        return jsonify({"answer": "من عيوني! دي الصورة اللي طلبتها:", "image": img_url})

    try:
        # استخدام موديل سريع ومستقر
        response = requests.get(f"https://text.pollinations.ai/{user_m}?system={SYSTEM_PROMPT}", timeout=15)
        return jsonify({"answer": response.text})
    except:
        return jsonify({"answer": "السيرفر مضغوط شوية، ابعت رسالتك تاني حالا يا بطل!"})
