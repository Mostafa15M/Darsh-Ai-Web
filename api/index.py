from flask import Flask, render_template, request, jsonify
import requests, os, uuid, hashlib

# تعديل المسار ليعمل على Vercel
app = Flask(__name__, template_folder='../templates')

class PixWithAI:
    def __init__(self):
        self.base_url = "https://api.pixwith.ai/api"
        self.session_token = hashlib.md5(f"{uuid.uuid4()}".encode()).hexdigest() + "0"
        self.headers = {
            'origin': 'https://pixwith.ai',
            'referer': 'https://pixwith.ai/',
            'user-agent': 'Mozilla/5.0',
            'x-session-token': self.session_token
        }

    def process_all(self, file_path, prompt, model_id):
        try:
            h = self.headers.copy()
            h['content-type'] = 'application/json'
            r_url = requests.post(f"{self.base_url}/chats/pre_url", headers=h, 
                                  json={"image_name": "input.jpg", "content_type": "image/jpeg"}).json()
            
            s3 = r_url.get("data", {}).get("url", r_url)
            fields = s3.get("fields", {})
            files = [(k, (None, str(v))) for k, v in fields.items()]
            with open(file_path, 'rb') as f:
                files.append(('file', ('input.jpg', f.read(), 'image/jpeg')))
            requests.post(s3.get("url"), files=files)
            
            key = fields.get("key")
            requests.post(f"{self.base_url}/items/create", headers=h, json={
                "images": {"image1": key}, "prompt": prompt,
                "options": {"num_outputs": 1, "aspect_ratio": "16:9", "duration": 4, "sound": True}, 
                "model_id": model_id
            })
            return True
        except: return False

    def get_latest(self):
        try:
            r = requests.post(f"{self.base_url}/items/history", headers=self.headers, 
                              json={"tool_type": "3", "page": 0, "page_size": 1}).json()
            items = r.get("data", {}).get("items", [])
            if items and items[0].get("status") == 2:
                for res in items[0].get('result_urls', []):
                    if not res.get('is_input'): return res.get('hd') or res.get('sd')
            return None
        except: return None

pix = PixWithAI()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    img = request.files['image']
    prompt = request.form.get('prompt')
    model = request.form.get('model')
    path = f"/tmp/{uuid.uuid4()}.jpg"
    img.save(path)
    pix.process_all(path, prompt, model)
    if os.path.exists(path): os.remove(path)
    return jsonify({"status": "processing"})

@app.route('/status')
def status():
    return jsonify({"url": pix.get_latest()})

# مهم جداً لـ Vercel
app = app
