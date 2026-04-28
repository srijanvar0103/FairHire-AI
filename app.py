from flask import Flask, render_template, request
import os
from PyPDF2 import PdfReader

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

skills_list = [
    "python", "java", "aws", "machine learning",
    "html", "css", "javascript", "sql", "react"
]

def extract_text_from_pdf(filepath):
    text = ""
    reader = PdfReader(filepath)
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text

@app.route("/", methods=["GET", "POST"])
def home():
    score = 0
    found_skills = []
    preview = None

    if request.method == "POST":
        file = request.files["resume"]

        if file:
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(filepath)

            resume_text = extract_text_from_pdf(filepath).lower()

            # Remove bias words
            bias_words = ["male", "female", "mr", "mrs", "he", "she"]
            for word in bias_words:
                resume_text = resume_text.replace(word, "")

            # Skill detection (no duplicates)
            for skill in skills_list:
                if skill in resume_text and skill not in found_skills:
                    score += 10
                    found_skills.append(skill)

            preview = resume_text[:500]

    return render_template(
        "index.html",
        score=score if request.method == "POST" else None,
        skills=found_skills,
        preview=preview
    )

if __name__ == "__main__":
    app.run(debug=True)