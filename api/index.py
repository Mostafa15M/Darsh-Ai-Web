from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__, template_folder='../templates')

SYSTEM_PROMPT = "أنت 'درش'، ذكاء اصطناعي مطوره مصطفى منصور. رد دايماً بالمصري وخليك سريع ومختصر."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    user_q = data.get('query', '').strip()
    
    # توليد الصور
    if any(word in user_q.lower() for word in ["ارسم", "صورة", "image"]):
        img_url = f"https://pollinations.ai/p/{user_q}?width=1024&height=1024&model=flux"
        return jsonify({"answer": "طلبك مجاب يا درش! دي الصورة:", "image": img_url})

    try:
        res = requests.get(f"https://text.pollinations.ai/{user_q}?system={SYSTEM_PROMPT}", timeout=10)
        return jsonify({"answer": res.text})
    except:
        return jsonify({"answer": "معلش يا مصطفى، السيرفر مهنج ثانية. جرب تبعت تاني!"})
