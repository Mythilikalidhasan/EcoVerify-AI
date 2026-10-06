# EcoVerify-AI

### E-Waste Certificate Verification Assistant

EcoVerify AI is a Streamlit-based application that uses OCR and automated validation to analyze e-waste recycling certificates. The system extracts important information from uploaded certificate images and checks for missing fields, inconsistent dates, invalid quantities, and duplicate certificate records.

> **Note:** EcoVerify AI performs preliminary document validation. It does not confirm whether a certificate is legally authentic or officially issued.

---

## Problem Statement

Organizations generate electronic waste such as laptops, desktop computers, monitors, printers, and other electronic equipment. Documentation related to the collection and recycling of this waste may contain important information that needs to be checked.

Manually reviewing multiple documents can be time-consuming and error-prone.

EcoVerify AI automates the initial document-checking process using OCR and rule-based validation.

---

## Key Features

* Upload PNG, JPG, or JPEG certificate images
* Extract text using Tesseract OCR
* Extract certificate number, company, recycler, quantity, and dates
* Detect missing required information
* Validate collection and recycling dates
* Validate e-waste quantity
* Detect duplicate certificate numbers
* Display a clear verification report
* Store processed certificate records locally

---

## Workflow

```text
Certificate Image
       ↓
Image Upload
       ↓
Image Preprocessing
       ↓
OCR Text Extraction
       ↓
Information Extraction
       ↓
Data Validation
       ↓
Duplicate Check
       ↓
Verification Report
```

---

## Technologies Used

| Technology    | Purpose                |
| ------------- | ---------------------- |
| Python        | Application logic      |
| Streamlit     | Web interface          |
| Tesseract OCR | Text extraction        |
| Pytesseract   | Python-OCR integration |
| OpenCV        | Image preprocessing    |
| Pillow        | Image processing       |
| Regex         | Information extraction |
| Pandas        | Record management      |
| CSV           | Local data storage     |

---

## work picture

<img width="1912" height="781" alt="image" src="https://github.com/user-attachments/assets/4d7595b4-9f35-4ac7-8612-75c48264eaad" />

## Information Extracted

The application extracts information such as:

```text
Certificate Number
Company Name
Recycler Name
E-Waste Quantity
Collection Date
Recycling Date
```

The extracted information is then validated using predefined rules.

---

## Example Validation

If the certificate contains:

```text
Collection Date: 15-08-2026
Recycling Date: 10-08-2026
```

EcoVerify AI identifies the inconsistency:

```text
Review Required:
Recycling date occurs before collection date.
```

Similarly, missing fields and duplicate certificate numbers are flagged for review.

---

## Project Structure

```text
EcoVerify-AI/
│
├── app.py
├── requirements.txt
├── assets/
│   └── demo-certificate.png
└── README.md
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/your-username/EcoVerify-AI.git
cd EcoVerify-AI
```

Create and activate a virtual environment:

```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Make sure Tesseract OCR is installed and update its path in `app.py` if required.

Run the application:

```bash
python -m streamlit run app.py
```

---

## Limitations

EcoVerify AI does not determine whether a certificate is genuinely authentic. OCR can also produce incorrect text when certificate images are unclear, damaged, or poorly scanned.

The system is intended for **preliminary document validation**, not official regulatory verification.

The certificate included in this repository is a **demo/test document and is not an official certificate**.

---

## Future Improvements

* PDF certificate support
* LLM-based explanation of detected issues
* Advanced document understanding for different certificate formats
* Tampering and image-forensics detection
* Verification against authorized recycler databases
* MySQL/PostgreSQL database integration
* Cloud deployment
* Advanced analytics dashboard

---

## Author

**Mythili Kalidhasan**

B.Sc. Computer Science with Artificial Intelligence

## demo link: 
https://ecoverify-ai-7hrkqsll9amypc7blex85a.streamlit.app/
