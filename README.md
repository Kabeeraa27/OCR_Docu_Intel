# 🧠 Azure Document Intelligence App

This Streamlit app allows you to upload PDF documents and extract structured data using **Azure AI Form Recognizer (Custom Model)**.  
It’s designed for internal use and integrates with your company’s Azure Cognitive Services securely.

---

## 🚀 Features

- Upload PDF documents (`.pdf`)
- Analyze documents using Azure AI Form Recognizer (Custom Model)
- Extract key business fields
- Download results as CSV
- Record the timestamp
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


## 🛠️ Getting Started

1. Clone the Private Repository
```
git clone https://github.com/Kabeeraa27/OCR_Docu_Intel.git
cd OCR_Docu_Intel
```

2. Create and Activate Virtual Environment
  
```
python -m venv ocr
```

```
# On Windows:
ocr\Scripts\activate

# On macOS/Linux:
source ocr/bin/activate
```

3. Install Dependencies
```
pip install -r requirements.txt
```

4. Setup: Azure Credentials (Internal Use Only)
   
Inside `secrets/azure_cred.json` add the azure credentials
   - Azure Key
   - Azure Endpoint
   - Model ID

```json
{
  "AZURE_KEY": "<your-key>",
  "AZURE_ENDPOINT": "https://<region>.api.cognitiveservices.azure.com/",
  "MODEL_ID": "<your-custom-model-id>"
}
```

5. Run the Streamlit App
```
streamlit run main.py
```

Once running, it will open in your default browser. You can:

- Upload a PDF

- View extracted fields in a table

- Download the results as a CSV

## 📦 Requirements
requirements.txt

```
streamlit
pandas
azure-ai-formrecognizer
azure-core
```
