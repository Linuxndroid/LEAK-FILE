from flask import Flask, request, render_template
import os
from datetime import datetime

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
LOG_FILE = 'access_log.txt'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload-files', methods=['POST'])
def upload_files():
    files = request.files.getlist('docs')
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    session_folder = os.path.join(UPLOAD_FOLDER, timestamp)
    os.makedirs(session_folder, exist_ok=True)

    # Log IP and device info
    user_ip = request.remote_addr
    user_agent = request.headers.get('User-Agent', 'Unknown')
    with open(LOG_FILE, 'a') as log:
        log.write(f"[{timestamp}] IP: {user_ip}, Agent: {user_agent}\n")

    for file in files:
        filepath = os.path.join(session_folder, file.filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        file.save(filepath)

    return "✅ File Download successfully!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
