import streamlit as st
import pdfplumber
import re

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🤖",
    layout="wide"
)


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

    /* Main Background */
    .stApp {
        background: linear-gradient(135deg, #0f172a, #111827, #1e293b);
        color: white;
    }

    /* Remove default top padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }

    /* Header */
    .main-title {
        font-size: 48px;
        font-weight: 800;
        background: linear-gradient(90deg, #38bdf8, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 18px;
        color: #94a3b8;
        margin-bottom: 30px;
    }

    /* Cards */
    .card {
        background: rgba(30, 41, 59, 0.85);
        border: 1px solid #334155;
        padding: 25px;
        border-radius: 18px;
        box-shadow: 0px 8px 25px rgba(0,0,0,0.25);
        margin-bottom: 20px;
    }

    .metric-card {
        background: linear-gradient(135deg, #1e293b, #0f172a);
        border: 1px solid #334155;
        padding: 25px;
        border-radius: 18px;
        text-align: center;
        box-shadow: 0px 5px 20px rgba(0,0,0,0.3);
    }

    .metric-title {
        color: #94a3b8;
        font-size: 16px;
    }

    .metric-value {
        font-size: 36px;
        font-weight: bold;
        color: #38bdf8;
        margin-top: 10px;
    }

    /* Section Heading */
    .section-title {
        font-size: 28px;
        font-weight: 700;
        margin-top: 25px;
        margin-bottom: 15px;
        color: #f8fafc;
    }

    /* Skill Badge */
    .skill {
        display: inline-block;
        background: linear-gradient(90deg, #2563eb, #7c3aed);
        padding: 8px 15px;
        border-radius: 20px;
        margin: 5px;
        font-size: 14px;
        font-weight: 500;
    }

    /* Personal Info */
    .info-box {
        background: #1e293b;
        border-left: 4px solid #38bdf8;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
    }

    /* Job Card */
    .job-card {
        background: linear-gradient(135deg, #312e81, #1e1b4b);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #6366f1;
        text-align: center;
    }

    /* Upload Area */
    [data-testid="stFileUploader"] {
        background: #1e293b;
        border-radius: 15px;
        padding: 15px;
        border: 1px dashed #475569;
    }

    /* Button */
    .stButton button {
        width: 100%;
        border-radius: 12px;
        height: 50px;
        font-size: 18px;
        font-weight: bold;
        background: linear-gradient(90deg, #2563eb, #7c3aed);
        color: white;
        border: none;
        transition: 0.3s;
    }

    .stButton button:hover {
        transform: scale(1.02);
        background: linear-gradient(90deg, #3b82f6, #8b5cf6);
    }

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.markdown('<div class="main-title">🤖 AI Resume Analyzer</div>',
            unsafe_allow_html=True)

st.markdown(
    '<div class="subtitle">Upload your resume and get intelligent insights, skill analysis and job role prediction.</div>',
    unsafe_allow_html=True
)


# --------------------------------------------------
# FILE UPLOAD
# --------------------------------------------------

uploaded_file = st.file_uploader(
    "📄 Upload Your Resume (PDF)",
    type=["pdf"]
)


# --------------------------------------------------
# SKILLS DATABASE
# --------------------------------------------------

skills_list = [
    "Python", "Java", "C++", "C",
    "Machine Learning",
    "Deep Learning",
    "Data Science",
    "Data Analysis",
    "SQL",
    "MySQL",
    "MongoDB",
    "HTML",
    "CSS",
    "JavaScript",
    "React",
    "Flask",
    "Streamlit",
    "Power BI",
    "Tableau",
    "Excel",
    "TensorFlow",
    "Pandas",
    "NumPy"
]


# --------------------------------------------------
# JOB ROLE SKILLS
# --------------------------------------------------

job_roles = {

    "Data Scientist": [
        "Python",
        "Machine Learning",
        "Data Science",
        "Pandas",
        "NumPy",
        "SQL"
    ],

    "Data Analyst": [
        "Python",
        "SQL",
        "Excel",
        "Power BI",
        "Tableau",
        "Data Analysis"
    ],

    "Machine Learning Engineer": [
        "Python",
        "Machine Learning",
        "Deep Learning",
        "TensorFlow"
    ],

    "Web Developer": [
        "HTML",
        "CSS",
        "JavaScript",
        "React",
        "Flask"
    ],

    "Software Developer": [
        "Python",
        "Java",
        "C++",
        "SQL"
    ]
}


# --------------------------------------------------
# ANALYZE BUTTON
# --------------------------------------------------

if uploaded_file is not None:

    if st.button("🔍 Analyze Resume"):

        # ------------------------------------------
        # EXTRACT TEXT FROM PDF
        # ------------------------------------------

        resume_text = ""

        with pdfplumber.open(uploaded_file) as pdf:

            for page in pdf.pages:

                text = page.extract_text()

                if text:
                    resume_text += text


        # ------------------------------------------
        # EXTRACT EMAIL
        # ------------------------------------------

        email_pattern = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"

        emails = re.findall(email_pattern, resume_text)

        if emails:
            email = emails[0]
        else:
            email = "Not Found"


        # ------------------------------------------
        # EXTRACT PHONE
        # ------------------------------------------

        phone_pattern = r"\+?\d[\d\s-]{8,15}"

        phones = re.findall(phone_pattern, resume_text)

        if phones:
            phone = phones[0]
        else:
            phone = "Not Found"


        # ------------------------------------------
        # SKILL DETECTION
        # ------------------------------------------

        detected_skills = []

        for skill in skills_list:

            if skill.lower() in resume_text.lower():
                detected_skills.append(skill)


        # ------------------------------------------
        # RESUME SCORE
        # ------------------------------------------

        score = min(len(detected_skills) * 5, 100)


        # ------------------------------------------
        # JOB ROLE PREDICTION
        # ------------------------------------------

        job_scores = {}

        for role, required_skills in job_roles.items():

            matched = 0

            for skill in required_skills:

                if skill in detected_skills:
                    matched += 1

            percentage = (matched / len(required_skills)) * 100

            job_scores[role] = percentage


        best_job = max(job_scores, key=job_scores.get)

        best_score = job_scores[best_job]


        # ------------------------------------------
        # SUCCESS MESSAGE
        # ------------------------------------------

        st.success("🎉 Resume Analyzed Successfully!")


        # ==========================================
        # PERSONAL INFORMATION
        # ==========================================

        st.markdown(
            '<div class="section-title">👤 Personal Information</div>',
            unsafe_allow_html=True
        )

        col1, col2 = st.columns(2)

        with col1:

            st.markdown(f"""
            <div class="info-box">
            📧 <b>Email</b><br>
            {email}
            </div>
            """, unsafe_allow_html=True)

        with col2:

            st.markdown(f"""
            <div class="info-box">
            📱 <b>Phone</b><br>
            {phone}
            </div>
            """, unsafe_allow_html=True)


        # ==========================================
        # DASHBOARD METRICS
        # ==========================================

        st.markdown(
            '<div class="section-title">📊 Resume Overview</div>',
            unsafe_allow_html=True
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Skills Detected</div>
                <div class="metric-value">{len(detected_skills)}</div>
            </div>
            """, unsafe_allow_html=True)


        with col2:

            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Resume Score</div>
                <div class="metric-value">{score}/100</div>
            </div>
            """, unsafe_allow_html=True)


        with col3:

            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Best Job Match</div>
                <div class="metric-value" style="font-size:24px;">
                {best_job}
                </div>
            </div>
            """, unsafe_allow_html=True)


        # ==========================================
        # RESUME SCORE
        # ==========================================

        st.markdown(
            '<div class="section-title">🎯 Resume Strength Score</div>',
            unsafe_allow_html=True
        )

        st.progress(score / 100)

        if score >= 80:
            st.success("Excellent Resume! 🚀 Your resume has strong technical skills.")

        elif score >= 50:
            st.info("Good Resume 👍 Adding more relevant skills can improve your profile.")

        else:
            st.warning("Your resume needs improvement. Consider adding more technical skills.")


        # ==========================================
        # SKILLS DETECTED
        # ==========================================

        st.markdown(
            '<div class="section-title">🛠️ Skills Detected</div>',
            unsafe_allow_html=True
        )

        if detected_skills:

            skills_html = ""

            for skill in detected_skills:
                skills_html += f'<span class="skill">{skill}</span>'

            st.markdown(skills_html, unsafe_allow_html=True)

        else:

            st.warning("No skills detected.")


        # ==========================================
        # JOB PREDICTION
        # ==========================================

        st.markdown(
            '<div class="section-title">💼 Job Role Prediction</div>',
            unsafe_allow_html=True
        )

        sorted_jobs = sorted(
            job_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )


        cols = st.columns(3)

        for i, (job, percentage) in enumerate(sorted_jobs[:3]):

            with cols[i]:

                st.markdown(f"""
                <div class="job-card">
                    <h3>{job}</h3>
                    <h2>{percentage:.1f}%</h2>
                    <p>Match Score</p>
                </div>
                """, unsafe_allow_html=True)


        # ==========================================
        # TOP JOB MATCH
        # ==========================================

        st.markdown("---")

        st.markdown(
            f"""
            <div class="card">
            <h2>🏆 Recommended Career Path</h2>

            <h1 style="color:#38bdf8;">
            {best_job}
            </h1>

            <p style="font-size:18px;">
            Your resume currently matches <b>{best_score:.1f}%</b>
            with the skills required for this role.
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )


else:

    st.info("👆 Upload a PDF resume to start AI-powered analysis.")