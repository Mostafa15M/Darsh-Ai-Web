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
            "user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36"
        }

    def search(self, query):
        try:
            params = {"q": query, "max_results": 10}
            res = requests.get(self.api_url, params=params, headers=self.headers, timeout=20)
            if res.status_code == 200:
                return res.json()
            return {"error": "سيرفر البحث لا يستجيب حالياً"}
        except Exception as e:
            return {"error": str(e)}

engine = DarshSearch()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_query = request.json.get('query')
    if not user_query:
        return jsonify({"error": "الرجاء إدخال سؤال"})
    
    result = engine.search(user_query)
    return jsonify(result)

app = app
