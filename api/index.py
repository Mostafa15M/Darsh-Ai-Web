from flask import Flask, render_template, request, jsonify
import requests, os, uuid, hashlib, time

app = Flask(__name__, template_folder='../templates')

class PixWithAI:
    def __init__(self):
        self.base_url = "https://api.pixwith.ai/api"
        self.session_token = hashlib.md5(f"{uuid.uuid4()}{int(time.time()*1000)}".encode()).hexdigest() + "0"
        self.headers = {
            'authority': 'api.pixwith.ai',
            'accept': '*/*',
            'origin': 'https://pixwith.ai',
            'referer': 'https://pixwith.ai/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'x-session-token': self.session_token
        }

    def _opts(self, url):
        try: requests.options(url, headers={'origin': 'https://pixwith.ai', 'referer': 'https://pixwith.ai/'}, timeout=5)
        except: pass

    def process_all(self, file_path, prompt, model_id):
        try:
            # Pre-URL
            self._opts(f"{self.base_url}/chats/pre_url")
            h = self.headers.copy()
            h['content-type'] = 'application/json'
            r_url = requests.post(f"{self.base_url}/chats/pre_url", headers=h, 
                                  json={"image_name": "input.jpg", "content_type": "image/jpeg"}).json()
            
            s3 = r_url.get("data", {}).get("url", r_url)
            url, fields = s3.get("url"), s3.get("fields", {})
            
            # Upload
            self._opts(url)
            files = [(k, (None, str(v))) for k, v in fields.items()]
            with open(file_path, 'rb') as f:
                files.append(('file', ('input.jpg', f.read(), 'image/jpeg')))
            requests.post(url, files=files, headers={'origin': 'https://pixwith.ai'})
            
            # Create Task
            self._opts(f"{self.base_url}/items/create")
            key = fields.get("key")
            requests.post(f"{self.base_url}/items/create", headers=h, json={
                "images": {"image1": key}, "prompt": prompt,
                "options": {"prompt_optimization": True, "num_outputs": 1, "aspect_ratio": "16:9", 
                           "resolution": "480p", "duration": 4, "sound": True}, "model_id": model_id
            })
            return True
        except: return False

    def get_latest_status(self):
        try:
            h = self.headers.copy()
            h['content-type'] = 'application/json'
            r = requests.post(f"{self.base_url}/items/history", headers=h, 
                            json={"tool_type": "3", "tag": "", "page": 0, "page_size": 1}).json()
            items = r.get("data", {}).get("items", [])
            if items:
                it = items[0]
                if it.get("status") == 2:
                    for res in it.get('result_urls', []):
                        if not res.get('is_input'):
                            return {"status": "success", "url": res.get('hd') or res.get('sd')}
                return {"status": "processing"}
            return {"status": "idle"}
        except: return {"status": "error"}

pix = PixWithAI()

@app.route('/')
def index(): return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    img = request.files['image']
    path = f"/tmp/{uuid.uuid4()}.jpg"
    img.save(path)
    success = pix.process_all(path, request.form.get('prompt'), request.form.get('model'))
    if os.path.exists(path): os.remove(path)
    return jsonify({"status": "started" if success else "error"})

@app.route('/status')
def status(): return jsonify(pix.get_latest_status())

app = app
