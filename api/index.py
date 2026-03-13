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
            # تقليل max_results لضمان سرعة الرد قبل الـ timeout
            params = {"q": query, "max_results": 5}
            res = requests.get(self.api_url, params=params, headers=self.headers, timeout=25)
            if res.status_code == 200:
                data = res.json()
                return data.get('answer') or data.get('result') or "ملقتش إجابة كافية، اسألني حاجة تانية يا درش."
            return "السيرفر عليه ضغط، جرب كمان ثواني."
        except:
            return "حصل مشكلة في الاتصال، جرب تاني يا بطل."

engine = DarshSearch()

@app.route('/')
def index(): return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    q = request.json.get('query')
    return jsonify({"answer": engine.search(q)})

app = app
