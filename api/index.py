from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__, template_folder='../templates')

class DarshSearch:
    def __init__(self):
        self.api_url = "https://contvia-test.onrender.com/api/research"
        self.headers = {
            "origin": "https://contvia.com",
            "referer": "https://contvia.com/",
            "accept": "application/json",
            "user-agent": "Mozilla/5.0 (Linux; Android 10)"
        }

    def search(self, query):
        try:
            params = {"q": query, "max_results": 15}
            res = requests.get(self.api_url, params=params, headers=self.headers, timeout=25)
            if res.status_code == 200:
                data = res.json()
                # فلترة الرد عشان ناخد الخلاصة بس
                return data.get('answer') or data.get('result') or "للأسف ملقيتش إجابة دقيقة للسؤال ده، جرب تسأل بطريقة تانية."
            return "السيرفر مشغول حالياً، جرب كمان شوية يا درش."
        except:
            return "حصل مشكلة في الاتصال، اتأكد من النت عندك."

engine = DarshSearch()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_query = request.json.get('query')
    if not user_query:
        return jsonify({"answer": "لازم تكتب سؤال عشان أقدر أبحث لك!"})
    
    response_text = engine.search(user_query)
    return jsonify({"answer": response_text})

app = app
