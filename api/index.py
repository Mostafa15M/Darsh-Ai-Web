from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__, template_folder='../templates')

class DarshSearch:
    def __init__(self):
        self.api_url = "https://contvia-test.onrender.com/api/research"
        self.headers = {"origin": "https://contvia.com", "user-agent": "Mozilla/5.0"}

    def search(self, query):
        # ردود ذكية وسريعة للتحيات عشان الموقع ميبانش بايظ
        greetings = ["هلا", "اهلا", "هاي", "صباح الخير", "مين انت"]
        if any(x in query.lower() for x in greetings):
            return "أهلاً بيك يا مصطفى! أنا محرك بحث دارش الذكي. اسألني عن أي معلومة محتاج تعرفها وهدورلك عليها فوراً."

        try:
            params = {"q": query, "max_results": 5}
            res = requests.get(self.api_url, params=params, headers=self.headers, timeout=20)
            if res.status_code == 200:
                data = res.json()
                return data.get('answer') or data.get('result') or "دورت كتير بس ملقتش إجابة دقيقة للسؤال ده، جرب تسأل بصيغة تانية."
            return "السيرفر تقيل شوية، جرب كمان ثواني."
        except:
            return "حاول تسأل سؤال كامل عشان أقدر أبحث لك صح."

engine = DarshSearch()

@app.route('/')
def index(): return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    q = request.json.get('query', '')
    return jsonify({"answer": engine.search(q)})

app = app
