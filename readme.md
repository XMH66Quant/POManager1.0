# 📄 Purchase Order Extractor

A lightweight web application to extract structured data from PDF purchase orders using AI.

---

## 🚀 Features

- Upload one or multiple PDF files
- Extract structured purchase order data
- Preview results instantly:
  - JSON format
  - CSV table
- Download results:
  - JSON
  - CSV
- Supports batch processing (multiple PDFs)
- Remembers API key and last selected files (browser storage)

---

## 🖥️ Demo UI

- Clean and simple interface
- AI model selection
- API key input
- Multi-file upload
- Result preview + download

---

## 📦 Installation

### 1. Clone repository

```bash
git clone git@github.com:XMH66Quant/POManager.git
cd <your-project-folder>
```

### 2. Create virtual environment (recommended)
python -m venv venv

source venv/bin/activate   # Mac/Linux

venv\Scripts\activate      # Windows

pip install -r requirements.txt

python app.py

http://127.0.0.1:5000