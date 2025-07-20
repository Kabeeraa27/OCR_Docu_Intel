# 🧠 Azure Document Intelligence Viewer (Streamlit App)

This Streamlit app allows you to upload PDF documents and extract structured data using **Azure AI Form Recognizer (Custom Model)**.  
It’s designed for internal use and integrates with your company’s Azure Cognitive Services securely.

---

## 🚀 Features

- Upload PDF documents (`.pdf`)
- Analyze documents using Azure AI Form Recognizer (Custom Model)
- Extract key business fields like:
  - Company Name
  - Directors
  - Registration Number
  - Signature Detection
- Download results as CSV

---

## 📁 Project Structure


```
OCR_DOCU_INTEL/
├── main.py # Streamlit App
├── requirements.txt # Python dependencies
├── .gitignore # Ignored files (secrets, venv, etc.)
├── README.md # You're here
└── secrets/
└── azure_cred.json # 🔐 Company credentials (not tracked)
```



## 🔐 Setup: Azure Credentials (Internal Use Only)

1. Ask your manager or admin for the file:  
   `secrets/azure_cred.json`

2. Place it inside a folder named `secrets` at the project root.

3. The file should follow this format:

```json
{
  "AZURE_KEY": "<your-key>",
  "AZURE_ENDPOINT": "https://<region>.api.cognitiveservices.azure.com/",
  "MODEL_ID": "<your-custom-model-id>"
}
```

## 🛠️ Getting Started

1. Clone the Private Repository
```
git clone https://github.com/your-username/your-private-repo.git
cd your-private-repo
```

2. Create and Activate Virtual Environment

```
python -m venv ocr

# On Windows:
ocr\Scripts\activate

# On macOS/Linux:
source ocr/bin/activate
```

3. Install Dependencies
```
pip install -r requirements.txt
```

4. Add Your Azure Credentials
Place the azure_cred.json file as described above.

5. Run the Streamlit App
```
streamlit run main.py
```

Once running, it will open in your default browser. You can:

- Upload a PDF

- View extracted fields in a table

- Download the results as a CSV

## 📦 Requirements
See requirements.txt. Key dependencies:

```
streamlit
pandas
azure-ai-formrecognizer
azure-core
```
