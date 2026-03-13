from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__, template_folder='../templates')

def get_ai_response(user_input):
    # ردود مخصصة ليك يا درش عشان الموقع يبقى براند باسمك
    q = user_input.lower()
    if "صاحب الصفحة" in q or "مين الي عملك" in q or "مين عملك" in q:
        return "صاحب الصفحة هو المبدع مصطفى منصور (درش)، وهو اللي صممني وطورني عشان أكون مساعده الذكي!"
    if "مين انت" in q or "انت مين" in q:
        return "أنا Darsh AI، محرك بحث ذكي طوره مصطفى منصور لمساعدة المستخدمين في الوصول للمعلومات بسرعة."
    
    try:
        # استخدام API بديل وسريع جداً للذكاء الاصطناعي العام
        url = f"https://api.popcat.xyz/chatbot?msg={user_input}&owner=Darsh&botname=DarshAI"
        res = requests.get(url, timeout=10)
        return res.json().get('response') if res.status_code == 200 else "السيرفر مشغول شوية، جرب تسأل تاني يا درش."
    except:
        return "حصل مشكلة في الاتصال، بس أنا معاك.. اسأل سؤالك تاني."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    q = request.json.get('query', '')
    if not q: return jsonify({"answer": "لازم تكتب حاجة عشان أبحث لك!"})
    return jsonify({"answer": get_ai_response(q)})

app = app
