import re
import io
import csv
import streamlit as st
import plotly.graph_objects as go

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="CVSync AI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# CUSTOM UI
# ============================================================

st.markdown(
    """
    <style>

    /* Main background */
    .stApp {
        background:
            radial-gradient(circle at 10% 10%, rgba(59,130,246,0.12), transparent 28%),
            radial-gradient(circle at 90% 20%, rgba(239,68,68,0.10), transparent 25%),
            linear-gradient(135deg, #f8fbff 0%, #eef4ff 50%, #fff7f7 100%);
    }

    /* Hide default menu */
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    /* Hero */
    .hero {
        background: linear-gradient(
            135deg,
            #0f172a 0%,
            #1d4ed8 48%,
            #dc2626 100%
        );
        padding: 32px 38px;
        border-radius: 26px;
        color: white;
        box-shadow: 0 15px 40px rgba(15,23,42,0.25);
        margin-bottom: 28px;
        position: relative;
        overflow: hidden;
    }

    .hero:before {
        content: "";
        position: absolute;
        width: 230px;
        height: 230px;
        border-radius: 50%;
        background: rgba(255,255,255,0.08);
        right: -60px;
        top: -80px;
    }

    .hero-logo {
        width: 72px;
        height: 72px;
        border-radius: 22px;
        background: linear-gradient(145deg,#ffffff,#dbeafe);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 38px;
        box-shadow:
            0 8px 0 rgba(0,0,0,0.15),
            0 15px 30px rgba(0,0,0,0.25);
        margin-bottom: 15px;
    }

    .hero-title {
        font-size: 42px;
        font-weight: 800;
        letter-spacing: -1px;
    }

    .hero-subtitle {
        font-size: 18px;
        opacity: 0.92;
        margin-top: 4px;
    }

    .hero-text {
        font-size: 15px;
        line-height: 1.7;
        max-width: 850px;
        margin-top: 15px;
    }

    /* Section cards */
    .section-card {
        background: rgba(255,255,255,0.88);
        border: 1px solid rgba(148,163,184,0.25);
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 8px 25px rgba(15,23,42,0.08);
        margin-bottom: 18px;
    }

    /* Skill chips */
    .chip {
        display: inline-block;
        padding: 6px 13px;
        margin: 4px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 600;
    }

    .ok {
        background: #dcfce7;
        color: #166534;
        border: 1px solid #86efac;
    }

    .no {
        background: #fee2e2;
        color: #991b1b;
        border: 1px solid #fca5a5;
    }

    .pf {
        background: #fef3c7;
        color: #92400e;
        border: 1px solid #fcd34d;
    }

    .ev {
        background: #eff6ff;
        border-left: 4px solid #2563eb;
        padding: 10px 14px;
        margin: 7px 0;
        border-radius: 8px;
        color: #1e293b;
        font-size: 14px;
    }

    /* Metrics */
    div[data-testid="stMetric"] {
        background: rgba(255,255,255,0.85);
        padding: 15px;
        border-radius: 16px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 5px 18px rgba(15,23,42,0.06);
    }

    /* Buttons */
    .stButton > button {
        border-radius: 12px;
        font-weight: 650;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# SKILL DATABASE
# ============================================================

SKILLS = {
    "Python": ("Programming Languages", ["python", "python3"]),
    "Java": ("Programming Languages", ["java", "core java"]),
    "C++": ("Programming Languages", ["c++", "cpp"]),
    "C": ("Programming Languages", ["c programming", "c language"]),
    "JavaScript": ("Programming Languages", ["javascript", "js", "ecmascript"]),
    "TypeScript": ("Programming Languages", ["typescript"]),
    "R": ("Programming Languages", ["r programming", "r language"]),
    "Go": ("Programming Languages", ["golang"]),
    "SQL": ("Databases", ["sql", "t-sql", "pl/sql"]),
    "MySQL": ("Databases", ["mysql"]),
    "PostgreSQL": ("Databases", ["postgresql", "postgres"]),
    "MongoDB": ("Databases", ["mongodb", "mongo"]),
    "Firebase": ("Databases", ["firebase", "firestore"]),

    "Machine Learning": (
        "Data Science & ML",
        ["machine learning", "ml"]
    ),
    "Deep Learning": (
        "Data Science & ML",
        ["deep learning", "dl", "neural network", "neural networks"]
    ),
    "NLP": (
        "Data Science & ML",
        ["nlp", "natural language processing"]
    ),
    "Computer Vision": (
        "Data Science & ML",
        ["computer vision", "image processing", "opencv"]
    ),
    "Generative AI / LLMs": (
        "Data Science & ML",
        [
            "generative ai",
            "genai",
            "llm",
            "llms",
            "large language model",
            "langchain",
            "rag"
        ]
    ),
    "Statistics": (
        "Data Science & ML",
        ["statistics", "statistical analysis", "probability"]
    ),
    "Data Analysis": (
        "Data Science & ML",
        [
            "data analysis",
            "data analytics",
            "eda",
            "exploratory data analysis"
        ]
    ),
    "Data Visualization": (
        "Data Science & ML",
        [
            "data visualization",
            "data visualisation",
            "matplotlib",
            "seaborn",
            "plotly"
        ]
    ),
    "Feature Engineering": (
        "Data Science & ML",
        ["feature engineering"]
    ),

    "Pandas": ("Libraries & Frameworks", ["pandas"]),
    "NumPy": ("Libraries & Frameworks", ["numpy"]),
    "Scikit-learn": (
        "Libraries & Frameworks",
        ["scikit-learn", "sklearn", "scikit learn"]
    ),
    "TensorFlow": (
        "Libraries & Frameworks",
        ["tensorflow", "keras"]
    ),
    "PyTorch": (
        "Libraries & Frameworks",
        ["pytorch", "torch"]
    ),
    "Hugging Face": (
        "Libraries & Frameworks",
        ["hugging face", "huggingface", "transformers"]
    ),
    "FastAPI": (
        "Libraries & Frameworks",
        ["fastapi", "fast api"]
    ),
    "Flask": ("Libraries & Frameworks", ["flask"]),
    "Django": ("Libraries & Frameworks", ["django"]),
    "Streamlit": ("Libraries & Frameworks", ["streamlit"]),
    "React": (
        "Libraries & Frameworks",
        ["react", "reactjs", "react.js"]
    ),
    "HTML/CSS": (
        "Libraries & Frameworks",
        ["html", "css", "html5", "css3"]
    ),
    "REST APIs": (
        "Libraries & Frameworks",
        ["rest api", "rest apis", "restful api", "api development"]
    ),

    "Docker": (
        "Tools, Cloud & DevOps",
        ["docker", "containerization", "containers"]
    ),
    "Kubernetes": (
        "Tools, Cloud & DevOps",
        ["kubernetes", "k8s"]
    ),
    "AWS": (
        "Tools, Cloud & DevOps",
        ["aws", "amazon web services", "ec2", "s3", "sagemaker"]
    ),
    "Azure": ("Tools, Cloud & DevOps", ["azure"]),
    "GCP": (
        "Tools, Cloud & DevOps",
        ["gcp", "google cloud"]
    ),
    "Git/GitHub": (
        "Tools, Cloud & DevOps",
        ["git", "github", "gitlab", "version control"]
    ),
    "CI/CD": (
        "Tools, Cloud & DevOps",
        ["ci/cd", "cicd", "jenkins", "github actions"]
    ),
    "Linux": (
        "Tools, Cloud & DevOps",
        ["linux", "unix", "ubuntu"]
    ),
    "Power BI": (
        "Tools, Cloud & DevOps",
        ["power bi", "powerbi"]
    ),
    "Tableau": (
        "Tools, Cloud & DevOps",
        ["tableau"]
    ),
    "Excel": (
        "Tools, Cloud & DevOps",
        ["excel", "advanced excel"]
    ),
    "MLOps": (
        "Tools, Cloud & DevOps",
        ["mlops", "mlflow", "model deployment"]
    ),
    "Spark/Hadoop": (
        "Tools, Cloud & DevOps",
        ["spark", "pyspark", "hadoop"]
    ),

    "Data Structures & Algorithms": (
        "CS Fundamentals",
        ["data structures", "algorithms", "dsa"]
    ),
    "Operating Systems": (
        "CS Fundamentals",
        ["operating systems", "operating system"]
    ),
    "OOP": (
        "CS Fundamentals",
        ["oop", "oops", "object oriented", "object-oriented"]
    ),
    "DBMS": (
        "CS Fundamentals",
        ["dbms", "database management"]
    ),
    "Agile/Scrum": (
        "CS Fundamentals",
        ["agile", "scrum"]
    ),

    "Communication": (
        "Soft Skills",
        ["communication", "communication skills"]
    ),
    "Teamwork": (
        "Soft Skills",
        ["teamwork", "team player", "collaboration"]
    ),
    "Problem Solving": (
        "Soft Skills",
        ["problem solving", "problem-solving", "analytical thinking"]
    ),
}

# ============================================================
# EDUCATION
# ============================================================

EDU_PATTERNS = {
    "B.E / B.Tech": r"\b(b\.?\s?e\.?|b\.?\s?tech|bachelor(?:'s)?(?: of (?:engineering|technology))?)\b",
    "M.E / M.Tech": r"\b(m\.?\s?e\.?|m\.?\s?tech|master(?:'s)?(?: of (?:engineering|technology|science))?)\b",
    "Computer/AI/DS Degree": r"(computer science|information technology|artificial intelligence|data science|ai\s*&\s*ds|aids|cse)"
}

# ============================================================
# DEMO DATA
# ============================================================

SAMPLE_JD = """Job Title: Data Analyst (Fresher / Entry Level)

We are looking for a Data Analyst with 0-2 years of experience.

Requirements:
- Bachelor's degree in Computer Science, AI & Data Science, Statistics or related field
- Strong programming skills in Python and SQL
- Hands-on experience with Pandas, NumPy and Excel
- Knowledge of Data Analysis and Statistics
- Experience creating dashboards using Power BI or Tableau
- Good understanding of Data Visualization
- Familiarity with Git/GitHub
- Good communication and problem solving skills
"""

SAMPLE_RESUME = """SRI KUMAR
Chennai, India | sri@example.com | github.com/sri

EDUCATION
B.Tech in Artificial Intelligence and Data Science, 2023 - 2027
CGPA: 8.4

SKILLS
Python, SQL, Pandas, NumPy, Excel, Data Analysis,
Statistics, Matplotlib, Power BI, Git, GitHub,
Machine Learning, HTML, CSS

PROJECTS
Student Performance Analysis
- Analysed student performance data using Python and Pandas.
- Created visualizations using Matplotlib.
- Used SQL to analyse student records.

Sales Dashboard
- Cleaned sales data using Pandas and Excel.
- Created an interactive Power BI dashboard.
- Presented business insights to faculty.

EXPERIENCE
Data Analysis Intern, XYZ Technologies
- Cleaned and analysed sales data using Python, Pandas and Excel.
- Collaborated with a team and presented findings.

ACHIEVEMENTS
- Participated in college hackathon.
- Strong problem solving and communication skills.
"""

SAMPLE_BATCH = [
    "Python, SQL, Pandas, NumPy, Excel, Data Analysis, Statistics, Power BI, Git, GitHub. B.Tech Artificial Intelligence and Data Science. Communication skills.",

    "Python, SQL, Pandas, NumPy, Excel, Power BI, Tableau, Statistics. B.E Computer Science. Teamwork.",

    "Python, SQL, Pandas, NumPy, Data Analysis, Matplotlib, Git, GitHub. B.Tech Artificial Intelligence and Data Science. Problem solving.",

    "Java, MySQL, HTML, CSS, JavaScript, Git. B.E Computer Science.",

    "Python, Pandas, NumPy, Excel, SQL, Statistics, Power BI, Data Visualization. B.Tech Artificial Intelligence and Data Science. Communication skills.",

    "Python, Machine Learning, Deep Learning, TensorFlow, Pandas, NumPy, Git. B.Tech Artificial Intelligence and Data Science. Problem solving."
]

# ============================================================
# ROADMAP
# ============================================================

PROJECT_IDEAS = {
    "Python": "Build a small data analysis project using Python and publish it on GitHub.",
    "SQL": "Create a student or sales database and write 15 SQL queries using JOIN, GROUP BY and subqueries.",
    "Pandas": "Take a real-world CSV dataset and clean, transform and analyse it using Pandas.",
    "NumPy": "Implement basic statistical calculations and linear regression using NumPy.",
    "Data Analysis": "Perform EDA on a Kaggle dataset and prepare a one-page insights report.",
    "Statistics": "Perform hypothesis testing such as t-test and chi-square on a real dataset.",
    "Excel": "Create an Excel dashboard using PivotTables, charts and formulas.",
    "Power BI": "Build a 3-page interactive Power BI dashboard using a sales or student dataset.",
    "Tableau": "Create an interactive Tableau dashboard using a public dataset.",
    "Data Visualization": "Create an analytical dashboard using Matplotlib, Plotly or Power BI.",
    "Git/GitHub": "Upload two projects with README files, screenshots and proper documentation.",
    "Machine Learning": "Build an end-to-end ML project with EDA, feature engineering and model evaluation.",
    "Deep Learning": "Train a CNN on MNIST or CIFAR-10 and compare its performance.",
    "NLP": "Build a text classification project using TF-IDF and Machine Learning.",
    "Docker": "Dockerize a Python data or ML application and run it locally.",
    "AWS": "Deploy a small data or ML application using AWS.",
    "FastAPI": "Create a FastAPI service with a /predict endpoint.",
    "Flask": "Build a Flask application that displays data analysis results.",
    "REST APIs": "Build a CRUD REST API with validation and error handling."
}

DAY_TEMPLATE = [
    "Understand the basics of {s} and learn why it is used in industry.",
    "Set up {s} and follow a beginner hands-on tutorial.",
    "Learn the most commonly used features of {s}.",
    "Practise 5-10 small tasks using {s}.",
    "Start the mini-project and build the basic version.",
    "Complete the mini-project and improve the output.",
    "Upload the project to GitHub and prepare 3 interview questions on {s}."
]

LEVEL_WORDS = {
    "strong": (80, 101, "🟢 Strong Alignment"),
    "good": (60, 80, "🟡 Good Alignment"),
    "partial": (35, 60, "🟠 Partial Alignment"),
    "low": (0, 35, "🔴 Low Alignment")
}

# ============================================================
# PDF TEXT EXTRACTION
# ============================================================

def extract_pdf_text(file_bytes):
    text = ""

    try:
        import pdfplumber

        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                text += (page.extract_text() or "") + "\n"

    except Exception:
        text = ""

    if not text.strip():
        try:
            from pypdf import PdfReader

            reader = PdfReader(io.BytesIO(file_bytes))

            for page in reader.pages:
                text += (page.extract_text() or "") + "\n"

        except Exception:
            pass

    return text

# ============================================================
# HELPERS
# ============================================================

def term_regex(term):
    return re.compile(
        r"(?<![A-Za-z0-9+#])"
        + re.escape(term)
        + r"(?![A-Za-z0-9+#])",
        re.IGNORECASE
    )


def find_skills(text):
    found = set()

    for skill, (_, synonyms) in SKILLS.items():

        terms = set([skill.lower()] + synonyms)

        for term in terms:

            if skill in ("C", "R", "Go") and term == skill.lower():
                continue

            if term_regex(term).search(text):
                found.add(skill)
                break

    return found


def split_lines(text):
    lines = []

    for raw in re.split(r"[\n\r]+", text):

        raw = raw.strip(" -•*\t")

        if len(raw) > 3:
            lines.append(raw)

    return lines


def evidence_for(skill, resume_text, limit=2):

    synonyms = set([skill.lower()] + SKILLS[skill][1])

    output = []

    for line in split_lines(resume_text):

        for term in synonyms:

            if skill in ("C", "R", "Go") and term == skill.lower():
                continue

            if term_regex(term).search(line):
                output.append(line)
                break

        if len(output) >= limit:
            break

    return output


def parse_years(text):

    match = re.search(
        r"(\d+)\s*[-–to]+\s*(\d+)\s*\+?\s*years?",
        text,
        re.IGNORECASE
    )

    if match:
        return int(match.group(1)), int(match.group(2))

    match = re.search(
        r"(\d+)\s*\+?\s*years?",
        text,
        re.IGNORECASE
    )

    if match:
        return int(match.group(1)), int(match.group(1))

    if re.search(
        r"\bfresher|entry[- ]level|graduate\b",
        text,
        re.IGNORECASE
    ):
        return 0, 1

    return None


def resume_experience_signals(text):

    return {
        "internship": bool(
            re.search(r"\bintern(ship)?\b", text, re.IGNORECASE)
        ),

        "projects": len(
            re.findall(r"\bproject", text, re.IGNORECASE)
        ),

        "work": bool(
            re.search(
                r"\b(experience|worked|employed|engineer at|developer at)\b",
                text,
                re.IGNORECASE
            )
        )
    }


def detect_role(jd):

    match = re.search(
        r"(?:job title|role|position)\s*[:\-]\s*(.+)",
        jd,
        re.IGNORECASE
    )

    if match:
        return match.group(1).strip()

    first = jd.strip().split("\n")[0].strip()

    return first[:80] if first else "Not specified"


def detect_edu(text):

    return {
        key
        for key, pattern in EDU_PATTERNS.items()
        if re.search(pattern, text, re.IGNORECASE)
    }


def classify_jd_skills(jd, jd_skills):

    preferred = set()
    required = set()

    for skill in jd_skills:

        relevant_lines = []

        for line in split_lines(jd):

            terms = set([skill.lower()] + SKILLS[skill][1])

            for term in terms:

                if skill in ("C", "R", "Go") and term == skill.lower():
                    continue

                if term_regex(term).search(line):
                    relevant_lines.append(line)
                    break

        is_preferred = bool(relevant_lines) and all(
            re.search(
                r"\b(plus|preferred|nice to have|good to have|bonus|desirable|optional|familiar)\b",
                line,
                re.IGNORECASE
            )
            for line in relevant_lines
        )

        if is_preferred:
            preferred.add(skill)
        else:
            required.add(skill)

    return required, preferred

# ============================================================
# ANALYSIS ENGINE
# ============================================================

def analyse(resume, jd):

    jd_skills = find_skills(jd)
    resume_skills = find_skills(resume)

    required, preferred = classify_jd_skills(
        jd,
        jd_skills
    )

    matched_required = required & resume_skills
    matched_preferred = preferred & resume_skills

    missing_required = required - resume_skills
    missing_preferred = preferred - resume_skills

    extra = resume_skills - jd_skills

    total_weight = (
        len(required) * 1.0
        + len(preferred) * 0.5
    )

    gained_weight = (
        len(matched_required) * 1.0
        + len(matched_preferred) * 0.5
    )

    if total_weight:
        skill_score = gained_weight / total_weight * 100
    else:
        skill_score = 0

    years = parse_years(jd)
    signals = resume_experience_signals(resume)

    exp_score = 70
    exp_note = "No clear experience requirement found in JD."

    if years is not None:

        if years[1] <= 1:

            if signals["projects"] or signals["internship"]:
                exp_score = 100
                exp_note = "Fresher-level JD and resume shows projects/internship."
            else:
                exp_score = 60
                exp_note = "Fresher-level JD but limited project/internship proof."

        else:

            if signals["work"] and signals["internship"]:
                exp_score = 85
            elif signals["work"] or signals["internship"]:
                exp_score = 55
            else:
                exp_score = 35

            exp_note = (
                f"JD asks around {years[0]}-{years[1]} years. "
                "Resume contains some experience evidence."
            )

    resume_edu = detect_edu(resume)
    jd_edu = detect_edu(jd)

    if jd_edu:

        if resume_edu & jd_edu:
            edu_score = 100
            edu_note = "Education requirement matches."
        else:
            edu_score = 50
            edu_note = "Education requirement is not clearly matched."

    else:
        edu_score = 80
        edu_note = "No clear education requirement found."

    final_score = round(
        0.70 * skill_score
        + 0.20 * exp_score
        + 0.10 * edu_score
    )

    label = "🔴 Low Alignment"

    for _, (low, high, name) in LEVEL_WORDS.items():

        if low <= final_score < high:
            label = name
            break

    return {
        "role": detect_role(jd),
        "final": final_score,
        "label": label,
        "skill_score": round(skill_score),
        "exp_score": exp_score,
        "exp_note": exp_note,
        "edu_score": edu_score,
        "edu_note": edu_note,
        "required": required,
        "preferred": preferred,
        "matched_req": matched_required,
        "matched_pref": matched_preferred,
        "missing_req": missing_required,
        "missing_pref": missing_preferred,
        "extra": extra,
        "jd_skills": jd_skills,
        "res_skills": resume_skills
    }

# ============================================================
# ROADMAP
# ============================================================

def priority_order(missing, required):

    return sorted(
        missing,
        key=lambda skill: (skill not in required, skill)
    )


def make_roadmap(skill):

    project = PROJECT_IDEAS.get(
        skill,
        f"Build a small practical project using {skill} and document it on GitHub."
    )

    days = [
        item.format(s=skill)
        for item in DAY_TEMPLATE
    ]

    return days, project

# ============================================================
# CHARTS
# ============================================================

def gauge(value):

    if value >= 80:
        color = "#22c55e"
    elif value >= 60:
        color = "#eab308"
    elif value >= 35:
        color = "#f97316"
    else:
        color = "#ef4444"

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=value,
            number={"suffix": "%"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": color},
                "steps": [
                    {
                        "range": [0, 35],
                        "color": "#fee2e2"
                    },
                    {
                        "range": [35, 60],
                        "color": "#ffedd5"
                    },
                    {
                        "range": [60, 80],
                        "color": "#fef9c3"
                    },
                    {
                        "range": [80, 100],
                        "color": "#dcfce7"
                    }
                ]
            },
            title={
                "text": "Resume–JD Alignment Score"
            }
        )
    )

    fig.update_layout(
        height=300,
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=10
        )
    )

    return fig


def category_chart(result):

    categories = {}

    for skill in result["jd_skills"]:

        category = SKILLS[skill][0]

        if category not in categories:
            categories[category] = [0, 0]

        categories[category][1] += 1

        if skill in result["res_skills"]:
            categories[category][0] += 1

    names = list(categories.keys())

    available = [
        categories[name][0]
        for name in names
    ]

    missing = [
        categories[name][1] - categories[name][0]
        for name in names
    ]

    fig = go.Figure()

    fig.add_bar(
        name="Available",
        x=names,
        y=available,
        marker_color="#2563eb"
    )

    fig.add_bar(
        name="Missing",
        x=names,
        y=missing,
        marker_color="#ef4444"
    )

    fig.update_layout(
        barmode="stack",
        height=320,
        title="Skill Coverage by Category",
        yaxis_title="Number of Skills"
    )

    return fig

# ============================================================
# REPORT
# ============================================================

def build_report(result):

    lines = [
        "CVSync AI - RESUME–JD ALIGNMENT REPORT",
        "=" * 50,
        f"Role: {result['role']}",
        f"Alignment Score: {result['final']}%",
        f"Level: {result['label']}",
        "",
        "PRESENT IN BOTH:",
        ", ".join(
            sorted(
                result["matched_req"]
                | result["matched_pref"]
            )
        ) or "None",
        "",
        "MISSING REQUIRED SKILLS:",
        ", ".join(
            sorted(result["missing_req"])
        ) or "None",
        "",
        "MISSING PREFERRED SKILLS:",
        ", ".join(
            sorted(result["missing_pref"])
        ) or "None",
        ""
    ]

    gaps = priority_order(
        result["missing_req"] | result["missing_pref"],
        result["required"]
    )

    for skill in gaps:

        days, project = make_roadmap(skill)

        lines.append(
            f"7-DAY PLAN: {skill}"
        )

        for number, day in enumerate(days, 1):
            lines.append(
                f"Day {number}: {day}"
            )

        lines.append(
            f"Mini Project: {project}"
        )

        lines.append("")

    return "\n".join(lines)

# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="hero">

        <div class="hero-logo">
            🎯
        </div>

        <div class="hero-title">
            CVSync AI
        </div>

        <div class="hero-subtitle">
            AI Resume Intelligence & Career Matching Platform
        </div>

        <div class="hero-text">
            Analyse your resume against real job descriptions,
            identify matching skills, discover missing skills,
            measure career alignment and get a personalised
            roadmap to improve your job readiness.
        </div>

    </div>
    """,
    unsafe_allow_html=True
)

st.caption(
    "CVSync AI · INTELLIQ SOLVEX · Department of AI&DS"
)

# ============================================================
# SESSION STATE
# ============================================================

if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""

if "jd_text" not in st.session_state:
    st.session_state.jd_text = ""

if "batch_sample" not in st.session_state:
    st.session_state.batch_sample = False

# ============================================================
# SINGLE RESUME VIEW
# ============================================================

def single_view():

    top1, top2 = st.columns([1, 4])

    with top1:

        if st.button(
            "⚡ Load Demo Data",
            use_container_width=True
        ):

            st.session_state.resume_text = SAMPLE_RESUME
            st.session_state.jd_text = SAMPLE_JD

            st.rerun()

    with top2:

        st.info(
            "Upload your Resume and paste the Job Description. "
            "Then click **Analyse Resume**."
        )

    left, right = st.columns(2)

    # --------------------------------------------------------
    # RESUME
    # --------------------------------------------------------

    with left:

        st.markdown(
            '<div class="section-card">',
            unsafe_allow_html=True
        )

        st.subheader("📄 1. Student Resume")

        resume_file = st.file_uploader(
            "Upload Resume (PDF or TXT)",
            type=["pdf", "txt"],
            key="resume_upload"
        )

        if resume_file is not None:

            data = resume_file.read()

            if resume_file.name.lower().endswith(".pdf"):

                extracted = extract_pdf_text(data)

            else:

                extracted = data.decode(
                    "utf-8",
                    errors="ignore"
                )

            if extracted.strip():

                st.session_state.resume_text = extracted

            else:

                st.warning(
                    "Could not extract text from this file."
                )

        st.session_state.resume_text = st.text_area(
            "Resume Text",
            value=st.session_state.resume_text,
            height=300,
            key="resume_text_box"
        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )

    # --------------------------------------------------------
    # JOB DESCRIPTION
    # --------------------------------------------------------

    with right:

        st.markdown(
            '<div class="section-card">',
            unsafe_allow_html=True
        )

        st.subheader("💼 2. Job Description")

        jd_file = st.file_uploader(
            "Upload JD (PDF or TXT)",
            type=["pdf", "txt"],
            key="jd_upload"
        )

        if jd_file is not None:

            data = jd_file.read()

            if jd_file.name.lower().endswith(".pdf"):

                extracted = extract_pdf_text(data)

            else:

                extracted = data.decode(
                    "utf-8",
                    errors="ignore"
                )

            if extracted.strip():
                st.session_state.jd_text = extracted

        st.session_state.jd_text = st.text_area(
            "Paste Job Description",
            value=st.session_state.jd_text,
            height=300,
            key="jd_text_box"
        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )

    # --------------------------------------------------------
    # ANALYSE
    # --------------------------------------------------------

    analyse_button = st.button(
        "🔍 Analyse Resume",
        type="primary",
        use_container_width=True
    )

    if not analyse_button:
        return

    if (
        not st.session_state.resume_text.strip()
        or not st.session_state.jd_text.strip()
    ):

        st.error(
            "Please provide both Resume and Job Description."
        )

        return

    result = analyse(
        st.session_state.resume_text,
        st.session_state.jd_text
    )

    if not result["jd_skills"]:

        st.warning(
            "No recognised skills were detected in the Job Description."
        )

    st.divider()

    st.header(
        f"🎯 Result for: {result['role']}"
    )

    chart1, chart2 = st.columns(2)

    with chart1:

        st.plotly_chart(
            gauge(result["final"]),
            use_container_width=True
        )

        st.subheader(
            result["label"]
        )

    with chart2:

        st.plotly_chart(
            category_chart(result),
            use_container_width=True
        )

    # --------------------------------------------------------
    # SCORE CARDS
    # --------------------------------------------------------

    m1, m2, m3 = st.columns(3)

    m1.metric(
        "Skills Alignment",
        f"{result['skill_score']}%"
    )

    m2.metric(
        "Experience Alignment",
        f"{result['exp_score']}%"
    )

    m3.metric(
        "Education Alignment",
        f"{result['edu_score']}%"
    )

    st.info(
        f"📌 {result['exp_note']}\n\n"
        f"🎓 {result['edu_note']}"
    )

    st.warning(
        "⚠️ This score represents Resume-to-JD alignment only. "
        "It is not a hiring probability or selection guarantee."
    )

    # --------------------------------------------------------
    # TABS
    # --------------------------------------------------------

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "✅ Skill Match",
            "🔎 Resume Evidence",
            "🗺️ Gap Roadmap",
            "💡 Extras & Tips"
        ]
    )

    # --------------------------------------------------------
    # TAB 1
    # --------------------------------------------------------

    with tab1:

        st.subheader(
            "Skills Present in Both"
        )

        matched = sorted(
            result["matched_req"]
            | result["matched_pref"]
        )

        st.markdown(
            "".join(
                f"<span class='chip ok'>✔ {skill}</span>"
                for skill in matched
            )
            or "_None_",
            unsafe_allow_html=True
        )

        st.subheader(
            "Required Skills Missing"
        )

        st.markdown(
            "".join(
                f"<span class='chip no'>✘ {skill}</span>"
                for skill in sorted(result["missing_req"])
            )
            or "_None 🎉_",
            unsafe_allow_html=True
        )

        if result["missing_pref"]:

            st.subheader(
                "Preferred Skills Missing"
            )

            st.markdown(
                "".join(
                    f"<span class='chip pf'>○ {skill}</span>"
                    for skill in sorted(result["missing_pref"])
                ),
                unsafe_allow_html=True
            )

        rows = []

        for skill in sorted(result["jd_skills"]):

            rows.append(
                {
                    "Skill": skill,
                    "Category": SKILLS[skill][0],
                    "Type": (
                        "Required"
                        if skill in result["required"]
                        else "Preferred"
                    ),
                    "Status": (
                        "Available"
                        if skill in result["res_skills"]
                        else "Missing"
                    )
                }
            )

        st.subheader(
            "Technical Skill Gap Table"
        )

        st.dataframe(
            rows,
            use_container_width=True,
            hide_index=True
        )

    # --------------------------------------------------------
    # TAB 2
    # --------------------------------------------------------

    with tab2:

        st.caption(
            "Evidence lines from your resume for matched skills."
        )

        matched_all = sorted(
            result["matched_req"]
            | result["matched_pref"]
        )

        if not matched_all:

            st.info(
                "No matching skills found."
            )

        for skill in matched_all:

            st.markdown(
                f"### {skill}"
            )

            evidence = evidence_for(
                skill,
                st.session_state.resume_text
            )

            if evidence:

                for line in evidence:

                    st.markdown(
                        f"<div class='ev'>“{line}”</div>",
                        unsafe_allow_html=True
                    )

            else:

                st.caption(
                    "No detailed evidence found."
                )

    # --------------------------------------------------------
    # TAB 3
    # --------------------------------------------------------

    with tab3:

        gaps = priority_order(
            result["missing_req"]
            | result["missing_pref"],
            result["required"]
        )

        if not gaps:

            st.success(
                "🎉 No skill gaps detected!"
            )

        for skill in gaps:

            days, project = make_roadmap(skill)

            tag = (
                "Required"
                if skill in result["required"]
                else "Nice-to-have"
            )

            with st.expander(
                f"📚 {skill} · {tag}",
                expanded=(skill == gaps[0])
            ):

                for number, day in enumerate(days, 1):

                    st.markdown(
                        f"**Day {number}:** {day}"
                    )

                st.success(
                    f"🛠️ Mini Project: {project}"
                )

    # --------------------------------------------------------
    # TAB 4
    # --------------------------------------------------------

    with tab4:

        st.subheader(
            "Extra Skills"
        )

        st.markdown(
            "".join(
                f"<span class='chip pf'>{skill}</span>"
                for skill in sorted(result["extra"])
            )
            or "_None_",
            unsafe_allow_html=True
        )

        st.subheader(
            "Suggested Improvements"
        )

        tips = []

        if result["missing_req"]:

            important = priority_order(
                result["missing_req"],
                result["required"]
            )[:3]

            tips.append(
                "Focus first on: "
                + ", ".join(important)
                + "."
            )

        tips.append(
            "Add measurable results to project descriptions "
            "such as accuracy, users, time saved or performance."
        )

        tips.append(
            "Use relevant keywords from the JD truthfully in your resume."
        )

        tips.append(
            "Give project-based proof for important technical skills."
        )

        for tip in tips:

            st.markdown(
                f"• {tip}"
            )

    # --------------------------------------------------------
    # DOWNLOAD
    # --------------------------------------------------------

    st.download_button(
        "⬇️ Download Alignment Report",
        data=build_report(result),
        file_name="cv_sync_report.txt",
        mime="text/plain",
        use_container_width=True
    )

# ============================================================
# CAMPUS BATCH
# ============================================================

def batch_view():

    st.header(
        "🏫 Campus Batch Analysis"
    )

    st.caption(
        "Analyse multiple student resumes against one Job Description."
    )

    jd = st.text_area(
        "Job Description",
        value=st.session_state.jd_text,
        height=200,
        key="batch_jd_box"
    )

    files = st.file_uploader(
        "Upload Multiple Resumes",
        type=["pdf", "txt"],
        accept_multiple_files=True,
        key="batch_resume_upload"
    )

    sample_button = st.button(
        "⚡ Use Sample Batch"
    )

    if sample_button:

        st.session_state.batch_sample = True
        st.session_state.jd_text = SAMPLE_JD

        st.rerun()

    resumes = []

    if files:

        for file in files:

            data = file.read()

            if file.name.lower().endswith(".pdf"):

                text = extract_pdf_text(data)

            else:

                text = data.decode(
                    "utf-8",
                    errors="ignore"
                )

            if text.strip():
                resumes.append(text)

    elif st.session_state.batch_sample:

        resumes = SAMPLE_BATCH
        jd = SAMPLE_JD

    if not resumes:

        st.info(
            "Upload multiple resumes or click Use Sample Batch."
        )

        return

    if not jd.strip():

        st.error(
            "Please provide a Job Description."
        )

        return

    results = [
        analyse(resume, jd)
        for resume in resumes
    ]

    count = len(results)

    average = round(
        sum(result["final"] for result in results) / count
    )

    good_count = sum(
        1
        for result in results
        if result["final"] >= 60
    )

    # --------------------------------------------------------
    # METRICS
    # --------------------------------------------------------

    k1, k2, k3 = st.columns(3)

    k1.metric(
        "Students Analysed",
        count
    )

    k2.metric(
        "Average Alignment",
        f"{average}%"
    )

    k3.metric(
        "Strong / Good",
        f"{good_count} / {count}"
    )

    # --------------------------------------------------------
    # GAP ANALYSIS
    # --------------------------------------------------------

    all_skills = set()

    for result in results:
        all_skills.update(result["jd_skills"])

    gap_rows = []

    for skill in sorted(all_skills):

        have = sum(
            1
            for result in results
            if skill in result["res_skills"]
        )

        missing_percentage = round(
            (count - have) / count * 100
        )

        gap_rows.append(
            {
                "Skill": skill,
                "Missing %": missing_percentage,
                "Type": (
                    "Required"
                    if skill in results[0]["required"]
                    else "Preferred"
                )
            }
        )

    gap_rows.sort(
        key=lambda item: -item["Missing %"]
    )

    if gap_rows:

        figure = go.Figure(
            go.Bar(
                x=[
                    row["Missing %"]
                    for row in gap_rows
                ],
                y=[
                    row["Skill"]
                    for row in gap_rows
                ],
                orientation="h",
                marker_color="#2563eb"
            )
        )

        figure.update_layout(
            title="% of Students Missing Each Skill",
            xaxis_title="% of Batch Missing",
            height=max(
                350,
                35 * len(gap_rows)
            ),
            yaxis=dict(
                autorange="reversed"
            )
        )

        st.plotly_chart(
            figure,
            use_container_width=True
        )

    # --------------------------------------------------------
    # TRAINING RECOMMENDATION
    # --------------------------------------------------------

    top_gaps = [
        row["Skill"]
        for row in gap_rows
        if row["Missing %"] >= 50
    ]

    if top_gaps:

        st.warning(
            "🎯 Training recommendation: "
            + ", ".join(top_gaps[:5])
            + " are missing in more than half of the batch."
        )

    # --------------------------------------------------------
    # SCORE DISTRIBUTION
    # --------------------------------------------------------

    histogram = go.Figure(
        go.Histogram(
            x=[
                result["final"]
                for result in results
            ],
            nbinsx=10,
            marker_color="#dc2626"
        )
    )

    histogram.update_layout(
        title="Alignment Score Distribution",
        xaxis_title="Score (%)",
        yaxis_title="Students",
        height=300
    )

    st.plotly_chart(
        histogram,
        use_container_width=True
    )

    # --------------------------------------------------------
    # RANKING
    # --------------------------------------------------------

    order = sorted(
        range(count),
        key=lambda index: -results[index]["final"]
    )

    ranking = []

    for index in order:

        result = results[index]

        ranking.append(
            {
                "Student": f"Student {index + 1}",
                "Alignment %": result["final"],
                "Level": result["label"],
                "Missing Required Skills": len(
                    result["missing_req"]
                ),
                "Top Gaps": ", ".join(
                    sorted(result["missing_req"])[:4]
                )
            }
        )

    st.subheader(
        "📊 Ranked Student List"
    )

    st.dataframe(
        ranking,
        use_container_width=True,
        hide_index=True
    )

    # --------------------------------------------------------
    # CSV DOWNLOAD
    # --------------------------------------------------------

    buffer = io.StringIO()

    writer = csv.DictWriter(
        buffer,
        fieldnames=list(ranking[0].keys())
    )

    writer.writeheader()
    writer.writerows(ranking)

    st.download_button(
        "⬇️ Download Batch Report",
        data=buffer.getvalue(),
        file_name="cv_sync_batch_report.csv",
        mime="text/csv",
        use_container_width=True
    )

# ============================================================
# MODE SELECTION
# ============================================================

st.markdown(
    "### 🚀 Choose Analysis Mode"
)

mode = st.radio(
    "Mode",
    [
        "👤 Single Resume",
        "🏫 Campus Batch"
    ],
    horizontal=True
)

if mode.startswith("👤"):

    single_view()

else:

    batch_view()

# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    """
    <div style="
        text-align:center;
        padding:15px;
        color:#64748b;
        font-size:13px;
    ">
        🎯 <b>CVSync AI</b> · INTELLIQ SOLVEX · Department of AI&DS<br>
        Real Campus Problems. Intelligent Solutions.
    </div>
    """,
    unsafe_allow_html=True
)
