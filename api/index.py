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
            # زيادة وقت الانتظار لـ 30 ثانية عشان نلحق الرد
            params = {"q": query, "max_results": 5}
            res = requests.get(self.api_url, params=params, headers=self.headers, timeout=30)
            if res.status_code == 200:
                data = res.json()
                # محاولة استخراج الإجابة بأكثر من طريقة
                ans = data.get('answer') or data.get('result')
                if ans: return ans
            return "دقيقة واحدة يا درش، بحاول أجمع لك أدق معلومات..."
        except:
            return "السيرفر عليه ضغط حالياً، بس أنا معاك.. اسأل تاني."

engine = DarshSearch()

@app.route('/')
def index(): return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    q = request.json.get('query')
    if not q: return jsonify({"answer": "اكتب أي حاجة في بالك!"})
    return jsonify({"answer": engine.search(q)})

app = app
