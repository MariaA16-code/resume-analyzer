# Resume Analyzer Web Application

A Flask-based Resume Analyzer web application that analyzes PDF resumes and provides:

- ATS Score
- Skill Gap Analysis
- Resume Suggestions
- Contact Information Extraction
- Role-Based Resume Evaluation

This project is designed as a mini project/FYP module using Python, Flask, NLP, and PDF processing.

---

# Features

- Upload PDF resumes
- Extract resume text from PDF
- Extract:
  - Name
  - Email
  - Phone number
  - Skills
- ATS Score Calculation
- Role-based analysis
- Missing skills detection
- Resume improvement suggestions
- Clean responsive UI

---

# Technologies Used

- Python
- Flask
- HTML5
- CSS3
- JavaScript
- spaCy NLP
- pdfplumber
- Regex

---

# Project Structure

```text
Resume-Analyzer/
│
├── app.py
├── requirements.txt
├── README.md
│
├── uploads/
│
├── templates/
│   └── index.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   │
│   └── js/
│       └── main.js
```

---

# Installation

## 1. Clone the Repository

```bash
git clone <repository-link>
```

---

## 2. Open Project Folder

```bash
cd Resume-Analyzer
```

---

## 3. Install Required Libraries

```bash
pip install -r requirements.txt
```

---

## 4. Install spaCy English Model

```bash
python -m spacy download en_core_web_sm
```

---

# Run the Application

```bash
python app.py
```

Server will start at:

```text
http://127.0.0.1:5000
```

Open it in your browser.

---

# ATS Score Logic

The ATS score is calculated based on:

- Skills found in resume
- Skills required for selected role

Formula used:

```text
ATS Score = (Matched Skills / Required Skills) × 100
```

---

# Future Improvements

- Resume download report
- Database integration
- User login system
- Advanced NLP analysis
- AI-based recommendations
- Resume ranking system

---

# Author

Maria Amir — Information Engineering Technology, Final Year University of Lahore