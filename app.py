# app.py
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
import requests
import time
from PIL import Image
import pandas as pd
from flask_cors import CORS
import logging
import mimetypes
import asyncio

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'csv', 'xlsx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16*1024*1024  # 16MB limit

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_file(file):
    try:
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        file_info = {
            "filename": filename,
            "filepath": filepath,
            "type": file.content_type,
            "size": os.path.getsize(filepath)
        }

        # Process different file types
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            with Image.open(filepath) as img:
                file_info.update({
                    "dimensions": img.size,
                    "format": img.format
                })
        elif filename.lower().endswith('.csv'):
            df = pd.read_csv(filepath)
            file_info["preview"] = df.head().to_html()
        elif filename.lower().endswith('.xlsx'):
            df = pd.read_excel(filepath)
            file_info["preview"] = df.head().to_html()

        return file_info
    except Exception as e:
        print(f"File processing error: {str(e)}")
        return None

def ask_ollama(prompt, context=None):
    try:
        url = "http://localhost:11434/api/generate"
        payload = {
            "model": "deepseek-r1:14b",
            "prompt": f"{prompt}\n\nContext: {context if context else 'No additional context'}",
            "stream": False,
            "options": {
                "temperature": 0.7,
                "max_tokens": 2000
            }
        }

        response = requests.post(
            url,
            json=payload,
            headers={'Content-Type': 'application/json'},
            timeout=300  # 5 minutes timeout for large models
        )

        if response.status_code != 200:
            return f"API Error: {response.status_code} - {response.text}"

        return response.json().get('response', 'No response generated')

    except requests.exceptions.Timeout:
        return "Error: Request timed out. Model might be busy or underpowered."
    except Exception as e:
        return f"Connection Error: {str(e)}. Make sure Ollama is running."

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def handle_upload():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if not allowed_file(file.filename):
        return jsonify({"error": "File type not allowed"}), 400

    file_info = process_file(file)
    if not file_info:
        return jsonify({"error": "File processing failed"}), 500

    return jsonify(file_info)

@app.route('/chat', methods=['POST'])
def handle_chat():
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({"error": "Invalid request format"}), 400

        start_time = time.time()
        response = ask_ollama(
            data['message'],
            data.get('file_context')
        )
        print(f"Response generated in {time.time()-start_time:.2f}s")
        
        return jsonify({"response": response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@app.errorhandler(Exception)
def handle_exception(e):
    logging.error(f"An error occurred: {str(e)}")
    return jsonify({"error": "An internal server error occurred"}), 500

def allowed_file(filename):
    mime_type, _ = mimetypes.guess_type(filename)
    return mime_type in ['image/png', 'image/jpeg', 'application/vnd.ms-excel', 'text/csv']

async def ask_ollama(prompt, context=None):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "deepseek-r1:14b",
        "prompt": f"{prompt}\n\nContext: {context or 'No additional context'}",
        "stream": False,
        "options": {
            "temperature": 0.7,
            "max_tokens": 2000
        }
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, json=payload) as response:
                if response.status != 200:
                    return f"API Error: {response.status} - {await response.text()}"
                return (await response.json()).get('response', 'No response generated')
        except asyncio.TimeoutError:
            return "Error: Request timed out. Model might be busy or underpowered."
        except Exception as e:
            return f"Connection Error: {str(e)}. Make sure Ollama is running."

def process_file(file):
    try:
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        file.save(filepath)

        # Use streaming for large files if needed
        if file.content_type == 'text/csv':
            df = pd.read_csv(filepath, chunksize=1000)
            preview = pd.concat(chunk for chunk in df).head().to_html()
        elif file.content_type == 'application/vnd.ms-excel':
            df = pd.read_excel(filepath)
            preview = df.head().to_html()

        return {"filename": filename, "preview": preview}
    except Exception as e:
        logging.error(f"File processing error: {str(e)}")
        return None

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(host='0.0.0.0', port=5000, debug=True)