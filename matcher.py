from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# TF-IDF + Cosine Similarity Score
def calculate_match_score(resume_text, job_description):

    vectorizer = TfidfVectorizer()

    vectors = vectorizer.fit_transform(
        [resume_text, job_description]
    )

    similarity = cosine_similarity(
        vectors[0:1],
        vectors[1:2]
    )

    score = similarity[0][0] * 100

    return round(score, 2)


# Matched Skills + Missing Skills
def skill_analysis(resume_skills, job_skills):

    matched = []
    missing = []

    for skill in job_skills:

        if skill in resume_skills:
            matched.append(skill)
        else:
            missing.append(skill)

    return matched, missing


# Skill Match Score
def skill_match_score(matched, job_skills):

    if len(job_skills) == 0:
        return 0

    score = (len(matched) / len(job_skills)) * 100

    return round(score, 2)

from skill_groups import skill_groups

def related_skill_matches(resume_skills, missing_skills):

    related_matches = []

    for missing in missing_skills:

        for category, skills in skill_groups.items():

            if missing in skills:

                for resume_skill in resume_skills:

                    if resume_skill in skills and resume_skill != missing:

                        related_matches.append(
                            f"{resume_skill} → {missing}"
                        )

    return list(set(related_matches))