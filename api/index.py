from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__, template_folder='../templates')

# هنا بنستخدم API ذكي عشان يجاوب على كل حاجة
def get_ai_response(user_input):
    try:
        # ده API مجاني وسريع للذكاء الاصطناعي
        url = f"https://api.popcat.xyz/chatbot?msg={user_input}&owner=Darsh&botname=DarshAI"
        res = requests.get(url, timeout=15)
        if res.status_code == 200:
            return res.json().get('response')
        return "معلش، السيرفر مهنج شوية.. اسألني تاني."
    except:
        return "فيه مشكلة في الاتصال، جرب كمان شوية."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    q = request.json.get('query', '')
    if not q:
        return jsonify({"answer": "اكتب أي حاجة يا بطل!"})
    
    # الردود الخاصة بيك يا مصطفى (Customized)
    if "صاحب الصفحة" in q or "مين اللي عملك" in q:
        return jsonify({"answer": "صاحب الصفحة هو المبدع مصطفى منصور (درش)، وهو اللي طورني وبناني!"})
        
    response = get_ai_response(q)
    return jsonify({"answer": response})

app = app

