from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__, template_folder='../templates')

# تعليمات "درش" الثابتة
SYSTEM_PROMPT = "أنت ذكاء اصطناعي اسمك 'درش'. مطورك وصانعك هو المبدع مصطفى منصور Darsh Egypt. رد دايماً باللهجة المصرية وخليك شاطر ومرح."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    user_m = data.get('query', '').strip()
    image_data = data.get('image') # الصورة اللي المستخدم رفعها

    # 1. نظام توليد الصور (لو المستخدم طلب رسم)
    if any(word in user_m.lower() for word in ["ارسم", "صورة", "image", "draw", "صمم"]):
        img_url = f"https://pollinations.ai/p/{user_m}?width=1024&height=1024&model=flux&seed=42"
        return jsonify({
            "answer": "من عيوني يا درش! دي الصورة اللي تخيلتها ليك:",
            "image": img_url
        })

    # 2. نظام الدردشة وتحليل الصور (Vision) المجاني
    try:
        # بنبعت الطلب لمحرك يدعم النصوص والصور مع بعض
        payload = {
            "messages": [{"role": "user", "content": user_m}],
            "system": SYSTEM_PROMPT,
            "image": image_data if image_data else None,
            "model": "openai" # السيرفر هيختار أفضل موديل مجاني متاح
        }
        
        response = requests.post("https://text.pollinations.ai/", json=payload, timeout=20)
        return jsonify({"answer": response.text})
    except:
        return jsonify({"answer": "حصل ضغط على السيرفر المجاني، جرب تسألني تاني يا بطل!"})

app = app
