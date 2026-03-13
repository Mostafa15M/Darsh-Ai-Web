from flask import Flask, render_template, request, jsonify
import requests, os, uuid, hashlib

app = Flask(__name__, template_folder='../templates')

class PixWithAI:
    def __init__(self):
        self.base_url = "https://api.pixwith.ai/api"
        # توليد هوية جديدة تماماً في كل مرة لتجنب البلوك
        self.session_token = hashlib.md5(str(uuid.uuid4()).encode()).hexdigest() + "0"
        self.headers = {
            'accept': 'application/json, text/plain, */*',
            'origin': 'https://pixwith.ai',
            'referer': 'https://pixwith.ai/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'x-session-token': self.session_token
        }

    def process_all(self, file_path, prompt, model_id):
        try:
            # 1. الحصول على رابط الرفع
            h = self.headers.copy()
            r_url = requests.post(f"{self.base_url}/chats/pre_url", headers=h, 
                                  json={"image_name": "input.jpg", "content_type": "image/jpeg"}).json()
            
            s3_data = r_url.get("data", {}).get("url", {})
            url = s3_data.get("url")
            fields = s3_data.get("fields", {})
            
            # 2. رفع الصورة فعلياً لـ S3
            files = []
            for k, v in fields.items():
                files.append((k, (None, str(v))))
            with open(file_path, 'rb') as f:
                files.append(('file', ('input.jpg', f.read(), 'image/jpeg')))
            
            up_res = requests.post(url, files=files)
            if up_res.status_code > 204: return False
            
            # 3. أمر الإنشاء
            key = fields.get("key")
            create_res = requests.post(f"{self.base_url}/items/create", headers=h, json={
                "images": {"image1": key}, 
                "prompt": prompt,
                "options": {"num_outputs": 1, "aspect_ratio": "16:9", "duration": 4, "sound": True}, 
                "model_id": model_id
            })
            return create_res.status_code == 200
        except Exception as e:
            print(f"Error: {e}")
            return False

    def get_latest_status(self):
        try:
            r = requests.post(f"{self.base_url}/items/history", headers=self.headers, 
                              json={"tool_type": "3", "page": 0, "page_size": 1}).json()
            items = r.get("data", {}).get("items", [])
            if items:
                status = items[0].get("status") # 1 = processing, 2 = success, 3 = failed
                if status == 2:
                    urls = items[0].get('result_urls', [])
                    for res in urls:
                        if not res.get('is_input'):
                            return {"status": "success", "url": res.get('hd') or res.get('sd')}
                elif status == 3:
                    return {"status": "failed"}
                return {"status": "processing"}
            return {"status": "not_found"}
        except: return {"status": "error"}

pix = PixWithAI()

@app.route('/')
def index(): return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    img = request.files.get('image')
    if not img: return jsonify({"error": "No image"}), 400
    
    path = f"/tmp/{uuid.uuid4()}.jpg"
    img.save(path)
    success = pix.process_all(path, request.form.get('prompt', 'cinematic motion'), request.form.get('model', '3-38'))
    if os.path.exists(path): os.remove(path)
    
    return jsonify({"status": "started" if success else "error"})

@app.route('/status')
def status(): return jsonify(pix.get_latest_status())

app = app
