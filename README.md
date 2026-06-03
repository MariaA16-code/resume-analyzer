Resume Analyzer Web Application

A Flask-based Resume Analyzer that analyzes PDF resumes and provides:

- ATS Score
- Skill Gap Analysis
- Resume Suggestions
- Contact Information Extraction
- Role-Based Resume Evaluation

Features

- Upload PDF resumes
- Extract resume text from PDF
- Extract name, email, and phone number
- ATS score calculation
- Role-based analysis
- Missing skills detection
- Resume improvement suggestions

Technologies Used

- Python
- Flask
- HTML
- CSS
- JavaScript
- spaCy
- pdfplumber

Project Structure

Resume-Analyzer/
│
├── app.py
├── requirements.txt
├── uploads/
├── templates/
│   └── index.html
└── static/
    ├── css/
    │   └── style.css
    └── js/
        └── main.js

Installation

git clone <https://github.com/MariaA16-code/resume-analyzer.git>
cd Resume-Analyzer
pip install -r requirements.txt
python app.py