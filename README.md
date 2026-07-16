<div align="center">

# 🔎 MOSPI Semantic Search
**National Classification of Occupations (NCO) AI Engine**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/release/python-380/)
[![Flask](https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![FAISS](https://img.shields.io/badge/FAISS-Facebook_AI-blue?style=flat&logo=meta&logoColor=white)](https://github.com/facebookresearch/faiss)
[![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=flat&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

*An advanced, AI-powered semantic search engine for the Ministry of Statistics and Programme Implementation (MOSPI).*

</div>

---

## ✨ Overview

**MOSPI Semantic Search** revolutionizes how users interact with the **National Classification of Occupations (NCO)** dataset. By leveraging a state-of-the-art **multilingual-e5-large** embedding model and **FAISS** vector database, this engine allows users to query occupations using natural language—and even voice—delivering incredibly accurate, sub-millisecond results.

<div align="center">
  <!-- TODO: Replace this URL with an actual screenshot of the app once it's running -->
  <img src="https://via.placeholder.com/800x400/f8fafc/3b82f6?text=Screenshot+of+MOSPI+Search+App" alt="Web UI Preview" width="100%" style="border-radius: 10px; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);" />
</div>

---

## 🚀 Key Features

*   🧠 **SOTA Semantic Embeddings:** Powered by `intfloat/multilingual-e5-large` for profound semantic understanding of complex queries.
*   ⚡ **High-Performance Search:** Sub-millisecond retrieval speeds utilizing Facebook's **FAISS** vector similarity search.
*   🎙️ **Voice Integration:** Built-in Web Speech API support allows users to literally speak their queries directly into the browser.
*   📄 **Robust PDF Parsing:** A definitive extraction engine (`parser.py`) rigorously mines and cleans data from the original NCO PDF volumes.
*   🎨 **Beautiful UI:** A responsive, intuitive, and modern web interface crafted with **Tailwind CSS**.

---

## 🏗️ Architecture & Structure

```text
mospi-semantic-search/
├── 📂 data/                 # Raw PDFs and parsed nco_data.csv
├── 📂 app/                  # Application Core
│   ├── 📂 templates/        # Tailwind-powered HTML (index.html)
│   ├── 🐍 app.py            # Flask Web Server
│   ├── 🗂️ index.faiss       # Compiled FAISS vector index
│   └── 📊 lookup_data.csv   # Fast application-ready lookup data
├── 🐍 parser.py             # Extracts & cleans data from PDFs
├── 🐍 engine.py             # Generates E5 embeddings & FAISS index
├── 📜 requirements.txt      # Python dependencies
└── ⚙️ setup.bat & run.bat   # Windows automation scripts
```

---

## 🛠️ Getting Started

### Prerequisites

Ensure you have **Python 3.8+** installed. You will also need the original NCO PDF files placed inside the `data/` directory.

### 🪄 One-Click Setup (Windows)

The easiest way to get started. This script installs dependencies, parses the PDFs, and builds the AI engine automatically.

```cmd
setup.bat
```

### 🔨 Manual Setup

If you prefer to run things manually or are on macOS/Linux:

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Parse the PDF data:**
   ```bash
   python parser.py
   ```
   *(This extracts the raw occupations and creates `data/nco_data.csv`.)*

3. **Build the AI Search Engine:**
   ```bash
   python engine.py
   ```
   *(Generates vector embeddings and builds the FAISS index. May take a few minutes to download the E5 model).*

---

## 💻 Usage

### Start the Server
Launch the application using the batch script:
```cmd
run.bat
```
*Or manually via: `python app/app.py`*

### Querying
1. Navigate to `http://127.0.0.1:5000/` in your browser.
2. Type a natural language query like: *"a person who builds wooden furniture"*.
3. Click the **Microphone** icon to use voice search.
4. View your highly accurate, AI-matched NCO occupations!

---

<div align="center">
  <b>Built for the Ministry of Statistics and Programme Implementation (MOSPI)</b>
</div>
