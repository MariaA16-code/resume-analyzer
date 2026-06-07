from flask import Flask, render_template, request, jsonify
import pdfplumber
import os
import re
from werkzeug.utils import secure_filename

app = Flask(__name__)

# ───────────────── CONFIG ─────────────────
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB limit
os.makedirs('uploads', exist_ok=True)


# ───────────────── SKILLS DATABASE ─────────────────
SKILLS = [
    'python', 'flask', 'django', 'javascript', 'react',
    'html', 'css', 'sql', 'mysql', 'mongodb', 'postgresql',
    'machine learning', 'deep learning', 'tensorflow', 'pytorch',
    'scikit-learn', 'pandas', 'numpy', 'opencv', 'git', 'github',
    'linux', 'docker', 'rest api', 'flutter', 'dart',
    'java', 'c++', 'c#', 'php', 'nodejs', 'express',
    'data analysis', 'nlp', 'artificial intelligence'
]

# ───────────────── JOB ROLE SKILLS ─────────────────
JOB_SKILLS = {
    'Web Developer': [
        'html', 'css', 'javascript', 'react', 'flask',
        'django', 'mysql', 'git', 'rest api'
    ],

    'Data Scientist': [
        'python', 'pandas', 'numpy', 'scikit-learn',
        'machine learning', 'deep learning', 'sql', 'data analysis'
    ],

    'AI/ML Engineer': [
        'python', 'tensorflow', 'pytorch', 'scikit-learn',
        'opencv', 'nlp', 'machine learning', 'deep learning'
    ],

    'Backend Developer': [
        'python', 'flask', 'django', 'mysql',
        'postgresql', 'rest api', 'git', 'linux', 'docker'
    ],

    'Mobile Developer': [
        'flutter', 'dart', 'java', 'git', 'rest api'
    ]
}

# ───────────────── EXTRACT TEXT FROM PDF ─────────────────
def extract_text(pdf_path):
    text = ''

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ''

    return text


# ───────────────── EXTRACT NAME USING SPACY ─────────────────
def extract_name(text):
    lines = text.strip().split('\n')
    for line in lines[:5]:
        line = line.strip()
        if line and len(line.split()) <= 4 and line.replace(' ', '').isalpha():
            return line
    return 'Not found'


# ───────────────── EXTRACT EMAIL ─────────────────
def extract_email(text):
    match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)

    if match:
        return match.group()

    return 'Not found'


# ───────────────── EXTRACT PHONE ─────────────────
def extract_phone(text):
    match = re.search(r'(\+?\d[\d\s\-]{8,}\d)', text)

    if match:
        return match.group().strip()

    return 'Not found'


# ───────────────── EXTRACT SKILLS ─────────────────
def extract_skills(text):
    text_lower = text.lower()
    found_skills = []

    for skill in SKILLS:

        pattern = r'\b' + re.escape(skill) + r'\b'

        if re.search(pattern, text_lower):
            found_skills.append(skill)

    return found_skills


# ───────────────── ATS SCORE CALCULATION ─────────────────
def calculate_ats_score(found_skills, role):

    required_skills = JOB_SKILLS.get(role, [])

    if not required_skills:
        return 0, [], []

    matched_skills = [
        skill for skill in required_skills
        if skill in found_skills
    ]

    missing_skills = [
        skill for skill in required_skills
        if skill not in found_skills
    ]

    score = round(
        (len(matched_skills) / len(required_skills)) * 100
    )

    return score, matched_skills, missing_skills


# ───────────────── GENERATE SUGGESTIONS ─────────────────
def generate_suggestions(score, word_count, missing_skills):

    suggestions = []

    if score < 50:
        suggestions.append(
            'Add more relevant technical skills related to the selected role.'
        )

    if word_count < 150:
        suggestions.append(
            'Resume content is too short. Add more project and experience details.'
        )

    if missing_skills:
        suggestions.append(
            f'Missing important skills: {", ".join(missing_skills)}'
        )

    if score >= 80:
        suggestions.append(
            'Great resume! Your resume matches most ATS requirements.'
        )

    return suggestions


# ───────────────── HOME ROUTE ─────────────────
@app.route('/')
def index():
    return render_template('index.html')


# ───────────────── ANALYZE ROUTE ─────────────────
@app.route('/analyze', methods=['POST'])
def analyze():

    if 'resume' not in request.files:
        return jsonify({
            'error': 'No file uploaded'
        }), 400

    file = request.files['resume']

    role = request.form.get(
        'role',
        'Web Developer'
    )

    if file.filename == '':
        return jsonify({
            'error': 'No file selected'
        }), 400

    # PDF VALIDATION
    if not file.filename.lower().endswith('.pdf'):
        return jsonify({
            'error': 'Only PDF files are allowed'
        }), 400

    # SECURE FILE NAME
    filename = secure_filename(file.filename)

    filepath = os.path.join(
        app.config['UPLOAD_FOLDER'],
        filename
    )

    try:
        # SAVE FILE
        file.save(filepath)

        # EXTRACT TEXT
        text = extract_text(filepath)

        if not text.strip():
            return jsonify({
                'error': 'Could not extract text from PDF'
            }), 400

        # ANALYSIS
        name = extract_name(text)

        email = extract_email(text)

        phone = extract_phone(text)

        skills = extract_skills(text)

        score, matched_skills, missing_skills = calculate_ats_score(
            skills,
            role
        )

        word_count = len(text.split())

        suggestions = generate_suggestions(
            score,
            word_count,
            missing_skills
        )

        return jsonify({

            'name': name,

            'email': email,

            'phone': phone,

            'role': role,

            'skills_found': skills,

            'matched_skills': matched_skills,

            'missing_skills': missing_skills,

            'ats_score': score,

            'word_count': word_count,

            'suggestions': suggestions

        })

    finally:

        # DELETE FILE SAFELY
        if os.path.exists(filepath):
            os.remove(filepath)


# ───────────────── MAIN ─────────────────
import nltk
nltk.download('punkt', quiet=True)
if __name__ == '__main__':

    os.makedirs('uploads', exist_ok=True)

    app.run(debug=True)
    