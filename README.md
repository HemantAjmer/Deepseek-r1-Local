# **DeepSeek AI Assistant**

DeepSeek AI Assistant is a web application that integrates a chatbot with file processing capabilities. It allows users to upload and preview files, ask questions, and interact with AI in an intuitive interface.

---

## **Features**

- **AI Chatbot**: Powered by the DeepSeek model from Ollama.
- **File Uploads**: Process and preview supported file types (CSV, Excel, PNG, JPG).
- **Drag-and-Drop**: Easy file uploads with drag-and-drop functionality.
- **Dark/Light Mode**: Accessible theme toggle for a personalized experience.
- **Responsive Design**: Optimized for both mobile and desktop use.

---

## **Tech Stack**

### **Frontend**
- **HTML5/CSS3**: Clean and responsive design.
- **JavaScript**: Handles chat interactions, file uploads, and theme toggles.

### **Backend**
- **Python (Flask)**: Backend API and server-side logic.
- **aiohttp**: Asynchronous communication for AI model interactions.
- **Pandas**: File processing for CSV and Excel.
- **Pillow (PIL)**: Image processing.
- **Flask-CORS**: Cross-Origin Resource Sharing.

### **AI Model**
- **DeepSeek-R1:14b** from [Ollama](https://ollama.com/): A powerful AI model for natural language understanding.

---

## **Setup Instructions**

### **Step 1: Install Ollama**
1. Visit [Ollama](https://ollama.com/) and download the Ollama software for your operating system.
2. Follow the installation instructions provided on the website.

### **Step 2: Download DeepSeek Model**
1. Open a terminal and run the following command to pull the model:
   ```bash
   ollama pull deepseek-r1:14b
2. Verify the model is downloaded by listing all available models:
   ```bash
   ollama list
Step3: Start Ollama Server
   ```bash
  ollama serve
```
*Leave this terminal open as the server needs to run for the application to function.
### Step 4: Set Up and Run the Application:
## Prerequisites
  * Python 3.8 or later
  * pip (Python package installer)
  * Virtual environment (recommended)
## Installation
1. Clone it:
  ```bash
  git clone https://github.com/HemantAjmer/Deepseek-r1-Local.git
  cd deepseek-ai-assistant
```
2. Create a virtual environment and activate it:
  ```bash
  python -m venv venv
  source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
4. Start the Flask server:
   ```bash
   python app.py
5. Open your browser and go to:
   ```bash
   http://localhost:5000/
### Usage
## Chat with the AI
  * Enter your query in the input box and click "Send" to interact with the chatbot.
## Upload and Preview Files
  * Drag and drop files into the upload area or click to browse.
  * Supported file types:
    * CSV
    * Excel (XLSX)
    * Images (PNG, JPG, JPEG)
   
### Folder Structure
  ```bash
        deepseek-ai-assistant/
    │
    ├── app.py                   # Backend logic and Flask routes
    ├── templates/
    │   └── index.html           # Frontend HTML file
    ├── uploads/                 # Directory for uploaded files
    ├── requirements.txt         # Python dependencies
    └── README.md                # Project documentation
```
# Contact

Name: Hemant Choudhary
Email: Hemantchoudhary7415@gmail.com
GitHub: HemantAjmer

## Acknowledgements
  * [Ollama](https://ollama.com/)
  * [Flask](https://flask.palletsprojects.com/en/stable/)
  * [aiohttp]()
  * [Pandas](https://pandas.pydata.org/)
  * [Pillow](https://python-pillow.org/)
  * [FontAwesome](https://fontawesome.com/)
