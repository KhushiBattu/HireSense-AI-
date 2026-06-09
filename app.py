from matcher import related_skill_matches
from ats_score import calculate_ats_score
from recommendations import get_recommendations
from matcher import skill_analysis
from matcher import calculate_match_score
from matcher import skill_match_score
from role_predictor import predict_role, filter_role_skills

import streamlit as st
from parser import extract_text
from skills import extract_skills


# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="HireSense AI",
    page_icon="🤖",
    layout="wide"
)

# ---------------- CUSTOM CSS ---------------- #

st.markdown("""
<style>

/* Main Background */
.stApp{
    background: #0f172a;
    color: white;
}

/* Hero Section */
.hero{
    background: linear-gradient(135deg,#2563eb,#7c3aed);
    padding: 30px;
    border-radius: 20px;
    text-align: center;
    color: white;
    margin-bottom: 25px;
    box-shadow: 0px 8px 25px rgba(0,0,0,0.35);
}

.hero h1{
    font-size: 3rem;
    margin-bottom: 10px;
}

.hero p{
    font-size: 1.1rem;
    color: #e5e7eb;
}

/* Sidebar */
section[data-testid="stSidebar"]{
    background: #020617;
}

/* Metric Cards */
div[data-testid="metric-container"]{
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 16px;
    padding: 15px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.25);
}

/* Expander */
details{
    background: #1e293b;
    border-radius: 12px;
    padding: 8px;
}

/* Upload Box */
[data-testid="stFileUploader"]{
    background:#1e293b;
    border-radius:12px;
    padding:10px;
}

/* Text Area */
textarea{
    background-color:#1e293b !important;
    color:white !important;
}

/* Progress Bar */
div[data-testid="stProgressBar"]{
    height:18px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HERO SECTION ---------------- #

st.markdown("""
<div class="hero">

<h1>🤖 HireSense AI</h1>

<p>
AI-Powered Resume Screening & Career Recommendation System
</p>

</div>
""", unsafe_allow_html=True)

st.info(
    "Upload your resume and compare it against a job description to receive ATS scoring, role prediction, and improvement suggestions."
)

# ---------------- SIDEBAR ---------------- #

with st.sidebar:

    st.header("📄 Resume Upload")

    uploaded_file = st.file_uploader(
        "Upload Resume",
        type=["pdf"]
    )

# ---------------- MAIN APP ---------------- #

if uploaded_file:

    text = extract_text(uploaded_file)

    skills = extract_skills(text)

    with st.expander("📌 Detected Skills", expanded=True):

        if skills:

            for skill in skills:
                st.write("✅", skill)

        else:
            st.warning("No skills detected.")

    st.markdown("---")

    job_description = st.text_area(
        "📋 Paste Job Description"
    )

    if job_description:

        # Extract Skills from JD

        job_skills = extract_skills(
            job_description
        )

        matched, missing = skill_analysis(
            skills,
            job_skills
        )

        semantic_score = calculate_match_score(
            text,
            job_description
        )

        score = skill_match_score(
            matched,
            job_skills
        )

        # ---------------- Resume Analysis ---------------- #

        st.subheader("📊 Resume Match Analysis")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Skill Match Score",
                f"{score}%"
            )

        with col2:
            st.metric(
                "Semantic Similarity",
                f"{semantic_score}%"
            )

        st.markdown("---")

        # ---------------- Skills Comparison ---------------- #

        col1, col2 = st.columns(2)

        with col1:

            st.subheader("✅ Matched Skills")

            if matched:

                for skill in matched:
                    st.success(skill)

            else:
                st.warning("No matched skills found.")

        with col2:

            st.subheader("❌ Missing Skills")

            if missing:

                for skill in missing:
                    st.error(skill)

            else:
                st.success("No missing skills.")

        # ---------------- Related Skills ---------------- #

        related = related_skill_matches(
            skills,
            missing
        )

        if related:

            st.subheader(
                "🔄 Related Skills Found"
            )

            for item in related:
                st.info(item)

        st.markdown("---")

        # ---------------- Role Prediction ---------------- #

        filtered_skills = filter_role_skills(
            skills
        )

        predicted_role, confidence, top_roles = predict_role(
            filtered_skills
        )

        st.subheader(
            "🎯 Recommended Role"
        )

        st.success(
            predicted_role
        )

        # ---------------- ATS Score ---------------- #

        ats_score = calculate_ats_score(
            matched,
            missing,
            related
        )

        coverage = 0

        if len(job_skills) > 0:

            coverage = (
                len(matched)
                / len(job_skills)
            ) * 100

        # ---------------- Analytics Dashboard ---------------- #

        st.subheader(
            "📈 Analytics Dashboard"
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "ATS Score",
                f"{ats_score}/100"
            )

        with col2:
            st.metric(
                "Prediction Confidence",
                f"{confidence}%"
            )

        with col3:
            st.metric(
                "Keyword Coverage",
                f"{round(coverage,2)}%"
            )

        st.markdown("---")

        # ---------------- Career Paths ---------------- #

        st.subheader(
            "🚀 Top Career Paths"
        )

        for role, prob in top_roles:

            st.write(f"**{role}**")

            st.progress(prob / 100)

            st.write(f"{prob}%")

        st.markdown("---")

        # ---------------- Coverage ---------------- #

        st.subheader(
            "📋 Keyword Coverage"
        )

        st.progress(
            coverage / 100
        )

        st.write(
            f"{round(coverage,2)}% Coverage"
        )

        st.markdown("---")

        # ---------------- Recommendations ---------------- #

        recommendations = get_recommendations(
            skills
        )

        st.subheader(
            "💡 Resume Improvement Suggestions"
        )

        for rec in recommendations:

            st.info(rec)