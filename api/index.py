from flask import Flask, render_template, request, jsonify
import requests, os, time, uuid, hashlib

app = Flask(__name__, template_folder='../templates')

class PixWithAI:
    def __init__(self):
        self.base_url = "https://api.pixwith.ai/api"
        # توليد جلسة فريدة لكل مستخدم لمنع تداخل الطلبات
        self.session_token = hashlib.md5(f"{uuid.uuid4()}".encode()).hexdigest() + "0"
        self.headers = {
            'origin': 'https://pixwith.ai',
            'referer': 'https://pixwith.ai/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'x-session-token': self.session_token
        }

    def process_all(self, file_path, prompt, model_id):
        try:
            # 1. الحصول على رابط الرفع
            h = self.headers.copy()
            h['content-type'] = 'application/json'
            r_url = requests.post(f"{self.base_url}/chats/pre_url", headers=h, 
                                  json={"image_name": "input.jpg", "content_type": "image/jpeg"}).json()
            
            # 2. رفع الصورة
            s3 = r_url.get("data", {}).get("url", r_url)
            fields = s3.get("fields", {})
            files = [(k, (None, str(v))) for k, v in fields.items()]
            with open(file_path, 'rb') as f:
                files.append(('file', ('input.jpg', f.read(), 'image/jpeg')))
            requests.post(s3.get("url"), files=files)
            
            # 3. أمر إنشاء الفيديو
            key = fields.get("key")
            requests.post(f"{self.base_url}/items/create", headers=h, json={
                "images": {"image1": key}, "prompt": prompt,
                "options": {"num_outputs": 1, "aspect_ratio": "16:9", "duration": 4, "sound": True}, 
                "model_id": model_id
            })
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    def get_latest(self):
        try:
            r = requests.post(f"{self.base_url}/items/history", headers=self.headers, 
                              json={"tool_type": "3", "page": 0, "page_size": 1}).json()
            items = r.get("data", {}).get("items", [])
            if items and items[0].get("status") == 2:
                for res in items[0].get('result_urls', []):
                    if not res.get('is_input'): return res.get('hd') or res.get('sd')
            return None
        except:
            return None

pix = PixWithAI()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    img = request.files['image']
    prompt = request.form.get('prompt')
    model = request.form.get('model')
    
    path = os.path.join("/tmp", f"{uuid.uuid4()}.jpg")
    img.save(path)
    
    try:
        pix.process_all(path, prompt, model)
        return jsonify({"status": "processing"})
    finally:
        if os.path.exists(path): os.remove(path)

@app.route('/status')
def status():
    return jsonify({"url": pix.get_latest()})

# محرك التشغيل لـ Vercel
def handler(environ, start_response):
    return app(environ, start_response)
