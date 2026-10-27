🎯 CVSync AI

AI-Powered Resume Analysis, Job Matching & Skill Gap Analyzer

CVSync AI is a Streamlit-based application that analyzes a student's resume against a Job Description (JD). It identifies matching skills, missing skills, experience and education alignment, and provides a practical roadmap to improve the candidate's profile.

🚀 Features

- 📄 Upload Resume in PDF or TXT format
- 💼 Upload or paste Job Description
- 🎯 Resume–JD Alignment Score
- ✅ Matched Skills Detection
- ❌ Missing Required Skills Detection
- 💡 Preferred / Nice-to-have Skill Analysis
- 🔎 Resume Evidence for Matched Skills
- 🗺️ Skill Gap to 7-Day Learning Roadmap
- 📊 Skill Coverage Visualization
- 🏫 Campus Batch Analysis
- 📥 Download Analysis Reports
- 🔐 Anonymised Student Ranking for Batch Analysis

🛠️ Technologies Used

- Python
- Streamlit
- Plotly
- Regular Expressions
- PDFPlumber
- PyPDF

📌 How It Works

1. Upload or enter the student's resume.
2. Upload or paste the Job Description.
3. CVSync AI extracts relevant skills from both.
4. It compares the resume skills with the JD requirements.
5. It calculates an alignment score based on skills, experience and education.
6. It identifies skill gaps.
7. It generates a learning roadmap for the missing skills.

📊 Analysis

CVSync AI provides three major alignment indicators:

- Skills Alignment – How well the candidate's technical skills match the JD.
- Experience Alignment – Comparison of experience requirements with resume evidence.
- Education Alignment – Comparison of educational requirements with the resume.

«Note: The alignment score represents resume-to-job-description matching only. It is not a prediction of hiring probability or a guarantee of selection.»

🏫 Campus Batch Analysis

The Campus Batch mode allows multiple resumes to be analyzed against a single Job Description.

It provides:

- Average batch alignment
- Skill gaps across the batch
- Alignment score distribution
- Anonymised student ranking
- Training recommendations based on common missing skills
- Downloadable CSV report

▶️ Run Locally

Install the required packages:

pip install -r requirements.txt

Run the application:

streamlit run app.py

📁 Project Structure

CVSync-AI/
│
├── app.py
├── requirements.txt
└── README.md

🎓 Project Purpose

CVSync AI is designed to help students understand how well their resumes align with real-world job requirements and identify the skills they need to improve before applying for opportunities.

👨‍💻 Developed By

INTELLIQ SOLVEX
Department of Artificial Intelligence & Data Science

---

⭐ CVSync AI – Sync your CV with your career goals.
