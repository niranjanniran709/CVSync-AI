import re
import io
import csv
import streamlit as st
import plotly.graph_objects as go

# ===============================================================
# PAGE CONFIG
# ===============================================================

st.set_page_config(
    page_title="CVSync AI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ===============================================================
# GLOBAL CSS - BLUE + RED PREMIUM UI
# ===============================================================

st.markdown("""
<style>

html, body, [class*="css"] {
    font-family: "Segoe UI", sans-serif;
}

/* ---------- MAIN BACKGROUND ---------- */

.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(37,99,235,0.18), transparent 28%),
        radial-gradient(circle at 90% 15%, rgba(239,68,68,0.15), transparent 25%),
        linear-gradient(135deg, #f7f9ff 0%, #eef4ff 48%, #fff5f5 100%);
}

/* ---------- HIDE STREAMLIT DEFAULT ---------- */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    background: transparent !important;
}

/* ---------- REMOVE TOP SPACE ---------- */

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1450px;
}

/* ---------- HERO ---------- */

.hero {
    position: relative;
    overflow: hidden;
    padding: 55px 30px 50px 30px;
    border-radius: 30px;
    margin-bottom: 30px;

    background:
        radial-gradient(circle at 15% 20%, rgba(255,255,255,0.25), transparent 25%),
        radial-gradient(circle at 85% 80%, rgba(255,255,255,0.15), transparent 25%),
        linear-gradient(135deg, #0f3cc9 0%, #2563eb 45%, #dc2626 100%);

    box-shadow:
        0 25px 60px rgba(30,64,175,0.25),
        inset 0 1px 0 rgba(255,255,255,0.35);

    color: white;
    text-align: center;
}

.hero::before {
    content: "";
    position: absolute;
    width: 300px;
    height: 300px;
    border-radius: 50%;
    background: rgba(255,255,255,0.07);
    top: -150px;
    left: -100px;
}

.hero::after {
    content: "";
    position: absolute;
    width: 350px;
    height: 350px;
    border-radius: 50%;
    background: rgba(255,255,255,0.06);
    bottom: -190px;
    right: -100px;
}

.hero-title {
    font-size: 4rem;
    font-weight: 900;
    letter-spacing: 2px;
    text-shadow:
        0 3px 0 #0b2c91,
        0 6px 12px rgba(0,0,0,0.30);
    margin: 10px 0;
}

.hero-subtitle {
    font-size: 1.25rem;
    font-weight: 600;
    opacity: 0.95;
}

.hero-text {
    max-width: 720px;
    margin: 18px auto 0 auto;
    font-size: 1rem;
    line-height: 1.7;
    opacity: 0.9;
}

/* ---------- 3D LOGO ---------- */

.logo3d {
    width: 120px;
    height: 120px;
    margin: 0 auto 15px auto;
    position: relative;
    transform-style: preserve-3d;
    transform: perspective(700px) rotateX(12deg) rotateY(-12deg);
}

.logo-back {
    position: absolute;
    width: 100px;
    height: 100px;
    left: 10px;
    top: 10px;
    border-radius: 28px;
    background: linear-gradient(145deg, #061b61, #123aa5);
    box-shadow:
        12px 14px 0 #06184e,
        18px 20px 25px rgba(0,0,0,0.35);
}

.logo-ring-outer {
    position: absolute;
    width: 92px;
    height: 92px;
    left: 14px;
    top: 14px;
    border-radius: 50%;
    border: 13px solid white;
    box-shadow:
        0 0 0 6px #ef4444,
        0 7px 15px rgba(0,0,0,0.25);
}

.logo-ring-inner {
    position: absolute;
    width: 43px;
    height: 43px;
    left: 38px;
    top: 38px;
    border-radius: 50%;
    background: linear-gradient(145deg, #ff5252, #b91c1c);
    border: 8px solid #ffffff;
    box-shadow:
        5px 6px 0 #7f1d1d,
        0 7px 15px rgba(0,0,0,0.30);
}

.logo-dot {
    position: absolute;
    width: 14px;
    height: 14px;
    left: 52px;
    top: 52px;
    border-radius: 50%;
    background: #2563eb;
    box-shadow: 3px 3px 0 #102c85;
}

/* arrow */

.logo-arrow {
    position: absolute;
    width: 65px;
    height: 12px;
    background: linear-gradient(90deg, #ffffff, #bfdbfe);
    left: 55px;
    top: 24px;
    transform: rotate(-42deg);
    border-radius: 8px;
    box-shadow: 5px 6px 0 #071b61;
}

.logo-arrow::after {
    content: "";
    position: absolute;
    right: -5px;
    top: -11px;
    width: 0;
    height: 0;
    border-left: 25px solid #ffffff;
    border-top: 17px solid transparent;
    border-bottom: 17px solid transparent;
}

/* ---------- SECTION CARDS ---------- */

.section-card {
    background: rgba(255,255,255,0.82);
    border: 1px solid rgba(37,99,235,0.15);
    border-radius: 20px;
    padding: 22px;
    box-shadow:
        0 10px 30px rgba(30,64,175,0.08);
    margin-bottom: 18px;
}

/* ---------- METRIC CARDS ---------- */

[data-testid="stMetric"] {
    background: white;
    border-radius: 18px;
    padding: 18px;
    border: 1px solid rgba(37,99,235,0.12);
    box-shadow: 0 8px 25px rgba(30,64,175,0.08);
}

/* ---------- BUTTONS ---------- */

.stButton > button {
    border-radius: 12px !important;
    font-weight: 700 !important;
    border: none !important;
    transition: all 0.2s ease !important;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(37,99,235,0.20);
}

/* Primary button */

button[kind="primary"] {
    background: linear-gradient(135deg, #2563eb, #dc2626) !important;
    color: white !important;
}

/* ---------- INPUTS ---------- */

textarea,
input {
    border-radius: 12px !important;
}

/* ---------- TABS ---------- */

button[data-baseweb="tab"] {
    font-weight: 700;
}

/* ---------- CHIPS ---------- */

.chip {
    display:inline-block;
    padding:5px 13px;
    margin:4px;
    border-radius:18px;
    font-size:0.88rem;
    font-weight:600;
}

.ok {
    background:#dcfce7;
    color:#166534;
    border:1px solid #86efac;
}

.no {
    background:#fee2e2;
    color:#991b1b;
    border:1px solid #fca5a5;
}

.pf {
    background:#dbeafe;
    color:#1e40af;
    border:1px solid #93c5fd;
}

.ev {
    background:#f8fafc;
    border-left:4px solid #2563eb;
    padding:9px 13px;
    margin:5px 0;
    border-radius:7px;
    color:#222;
    font-size:0.9rem;
}

/* ---------- INFO BOX ---------- */

.info-card {
    background: linear-gradient(
        135deg,
        rgba(37,99,235,0.10),
        rgba(239,68,68,0.08)
    );
    border: 1px solid rgba(37,99,235,0.15);
    padding: 18px;
    border-radius: 16px;
}

/* ---------- FOOTER ---------- */

.footer {
    text-align:center;
    padding:25px;
    color:#64748b;
    font-size:0.9rem;
}

</style>
""", unsafe_allow_html=True)


# ===============================================================
# SKILL DATABASE
# ===============================================================

SKILLS = {

    "Python": ("Programming Languages", ["python", "python3"]),
    "Java": ("Programming Languages", ["java", "core java"]),
    "C++": ("Programming Languages", ["c++", "cpp"]),
    "C": ("Programming Languages", ["c programming", "c language"]),
    "JavaScript": ("Programming Languages", ["javascript", "js", "ecmascript"]),
    "TypeScript": ("Programming Languages", ["typescript"]),
    "R": ("Programming Languages", ["r programming", "r language"]),
    "Go": ("Programming Languages", ["golang"]),
    "Scala": ("Programming Languages", ["scala"]),
    "Bash/Shell": ("Programming Languages", ["bash", "shell scripting", "shell"]),

    "SQL": ("Databases", ["sql", "t-sql", "pl/sql"]),
    "MySQL": ("Databases", ["mysql"]),
    "PostgreSQL": ("Databases", ["postgresql", "postgres"]),
    "MongoDB": ("Databases", ["mongodb", "mongo"]),
    "Redis": ("Databases", ["redis"]),
    "SQLite": ("Databases", ["sqlite"]),
    "Firebase": ("Databases", ["firebase", "firestore"]),

    "Machine Learning": ("Data Science & ML", ["machine learning", "ml"]),
    "Deep Learning": ("Data Science & ML", [
        "deep learning", "dl", "neural network", "neural networks"
    ]),
    "NLP": ("Data Science & ML", [
        "nlp", "natural language processing"
    ]),
    "Computer Vision": ("Data Science & ML", [
        "computer vision", "cv", "image processing", "opencv"
    ]),
    "Generative AI / LLMs": ("Data Science & ML", [
        "generative ai", "genai", "llm", "llms",
        "large language model", "large language models",
        "langchain", "rag"
    ]),
    "Statistics": ("Data Science & ML", [
        "statistics", "statistical analysis", "probability"
    ]),
    "Data Analysis": ("Data Science & ML", [
        "data analysis", "data analytics", "eda",
        "exploratory data analysis"
    ]),
    "Data Visualization": ("Data Science & ML", [
        "data visualization", "data visualisation",
        "matplotlib", "seaborn", "plotly"
    ]),
    "Feature Engineering": ("Data Science & ML", [
        "feature engineering"
    ]),

    "Pandas": ("Libraries & Frameworks", ["pandas"]),
    "NumPy": ("Libraries & Frameworks", ["numpy"]),
    "Scikit-learn": ("Libraries & Frameworks", [
        "scikit-learn", "sklearn", "scikit learn"
    ]),
    "TensorFlow": ("Libraries & Frameworks", [
        "tensorflow", "tf", "keras"
    ]),
    "PyTorch": ("Libraries & Frameworks", [
        "pytorch", "torch"
    ]),
    "Hugging Face": ("Libraries & Frameworks", [
        "hugging face", "huggingface", "transformers"
    ]),
    "FastAPI": ("Libraries & Frameworks", [
        "fastapi", "fast api"
    ]),
    "Flask": ("Libraries & Frameworks", ["flask"]),
    "Django": ("Libraries & Frameworks", ["django"]),
    "Streamlit": ("Libraries & Frameworks", ["streamlit"]),
    "React": ("Libraries & Frameworks", [
        "react", "reactjs", "react.js"
    ]),
    "Node.js": ("Libraries & Frameworks", [
        "node.js", "nodejs", "node js",
        "express.js", "expressjs"
    ]),
    "Spring Boot": ("Libraries & Frameworks", [
        "spring boot", "springboot", "spring"
    ]),
    "HTML/CSS": ("Libraries & Frameworks", [
        "html", "css", "html5", "css3"
    ]),
    "REST APIs": ("Libraries & Frameworks", [
        "rest api", "rest apis", "restful",
        "restful api", "api development"
    ]),

    "Docker": ("Tools, Cloud & DevOps", [
        "docker", "containerization", "containers"
    ]),
    "Kubernetes": ("Tools, Cloud & DevOps", [
        "kubernetes", "k8s"
    ]),
    "AWS": ("Tools, Cloud & DevOps", [
        "aws", "amazon web services", "ec2",
        "s3 bucket", "sagemaker"
    ]),
    "Azure": ("Tools, Cloud & DevOps", ["azure"]),
    "GCP": ("Tools, Cloud & DevOps", [
        "gcp", "google cloud"
    ]),
    "Git/GitHub": ("Tools, Cloud & DevOps", [
        "git", "github", "gitlab", "version control"
    ]),
    "CI/CD": ("Tools, Cloud & DevOps", [
        "ci/cd", "cicd", "jenkins", "github actions"
    ]),
    "Linux": ("Tools, Cloud & DevOps", [
        "linux", "unix", "ubuntu"
    ]),
    "Power BI": ("Tools, Cloud & DevOps", [
        "power bi", "powerbi"
    ]),
    "Tableau": ("Tools, Cloud & DevOps", ["tableau"]),
    "Excel": ("Tools, Cloud & DevOps", [
        "excel", "advanced excel"
    ]),
    "MLOps": ("Tools, Cloud & DevOps", [
        "mlops", "mlflow", "model deployment"
    ]),
    "Spark/Hadoop": ("Tools, Cloud & DevOps", [
        "spark", "pyspark", "hadoop"
    ]),

    "Data Structures & Algorithms": ("CS Fundamentals", [
        "data structures", "algorithms", "dsa"
    ]),
    "Operating Systems": ("CS Fundamentals", [
        "operating systems", "operating system"
    ]),
    "OOP": ("CS Fundamentals", [
        "oop", "oops", "object oriented", "object-oriented"
    ]),
    "DBMS": ("CS Fundamentals", [
        "dbms", "database management"
    ]),
    "Agile/Scrum": ("CS Fundamentals", [
        "agile", "scrum"
    ]),
    "Communication": ("Soft Skills", [
        "communication", "communication skills"
    ]),
    "Teamwork": ("Soft Skills", [
        "teamwork", "team player", "collaboration", "collaborative"
    ]),
    "Problem Solving": ("Soft Skills", [
        "problem solving", "problem-solving", "analytical thinking"
    ]),
}


# ===============================================================
# EDUCATION
# ===============================================================

EDU_PATTERNS = {

    "B.E / B.Tech":
        r"\b(b\.?\s?e\.?|b\.?\s?tech|bachelor(?:'s)?(?: of (?:engineering|technology))?)\b",

    "M.E / M.Tech":
        r"\b(m\.?\s?e\.?|m\.?\s?tech|master(?:'s)?(?: of (?:engineering|technology|science))?)\b",

    "Computer/AI/DS Degree":
        r"(computer science|information technology|artificial intelligence|data science|ai\s*&\s*ds|aids|cse)",
}


# ===============================================================
# SAMPLE DATA
# ===============================================================

SAMPLE_JD = """Job Title: Data Analyst (Fresher / Entry Level)

We are looking for a Data Analyst with 0-2 years of experience to join our analytics team.

Requirements:
- Bachelor's degree in Computer Science, AI & Data Science, Statistics or related field
- Strong programming skills in Python and SQL
- Hands-on experience with Pandas, NumPy and Excel
- Knowledge of data cleaning, data analysis and exploratory data analysis
- Experience creating dashboards using Power BI or Tableau
- Knowledge of statistics and data visualization
- Familiarity with Git/GitHub
- Good communication skills and problem solving ability
"""

SAMPLE_RESUME = """SRI KUMAR
Chennai, India | sri@example.com | github.com/sri

EDUCATION
B.Tech in Artificial Intelligence and Data Science, 2023 - 2027
CGPA: 8.4

SKILLS
Python, SQL, Pandas, NumPy, Machine Learning, Scikit-learn,
Matplotlib, Power BI, Excel, Git, HTML, CSS

PROJECTS

Student Performance Predictor
- Built a Machine Learning model using Scikit-learn and Pandas
  to predict exam results with 87% accuracy.
- Cleaned and analysed student data using Python and Pandas.

Sales Dashboard
- Created an interactive Power BI dashboard for analysing
  monthly sales and regional performance.
- Used Excel and SQL for data preparation.

EXPERIENCE
Data Analysis Intern, XYZ Technologies (2 months)
- Cleaned and analysed sales data using Python, Pandas and Excel.
- Collaborated with a team of 4 and presented findings to the manager.

ACHIEVEMENTS
- Participated in college hackathon.
- Strong problem solving and communication skills.
"""


SAMPLE_BATCH = [

    "Python, SQL, Pandas, NumPy, Excel, Power BI, Data Analysis, Statistics. "
    "Built sales dashboard using Power BI. B.Tech Artificial Intelligence and Data Science. "
    "Good communication skills.",

    "Java, Spring Boot, MySQL, HTML, CSS, JavaScript. "
    "Built Library Management System. B.E Computer Science. Teamwork.",

    "Python, SQL, Pandas, NumPy, Power BI, Excel, Statistics, Data Analysis, "
    "Data Visualization, Git, GitHub. Built sales analytics dashboard. "
    "B.Tech Artificial Intelligence and Data Science.",

    "C, C++, Data Structures and Algorithms, Operating Systems, Linux, DBMS. "
    "Built file system simulator. B.E Computer Science and Engineering.",

    "Python, Pandas, NumPy, Matplotlib, Excel, SQL, Statistics, Data Analysis. "
    "Performed EDA on customer dataset. B.Tech Artificial Intelligence and Data Science.",

    "Python, PyTorch, Deep Learning, Computer Vision, OpenCV, Machine Learning, "
    "Pandas, NumPy, Git. Built face mask detection project. "
    "B.Tech Artificial Intelligence and Data Science. Teamwork."
]


# ===============================================================
# ROADMAP
# ===============================================================

PROJECT_IDEAS = {

    "Python":
        "Analyse a real-world CSV dataset using Python and create an insights report.",

    "SQL":
        "Design a 4-table database and write 15 queries using JOIN, GROUP BY and subqueries.",

    "Pandas":
