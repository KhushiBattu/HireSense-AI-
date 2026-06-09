import pandas as pd
import re

skills_df = pd.read_csv("data/skills.csv")

synonyms = {
    "powerbi": "Power BI",
    "sklearn": "Scikit-Learn",
    "scikit learn": "Scikit-Learn"
}

def extract_skills(text):

    found_skills = []

    text = text.lower()

    # Detect skills from skills.csv
    for skill in skills_df["skill"]:

        pattern = r"\b" + re.escape(str(skill).lower()) + r"\b"

        if re.search(pattern, text):
            found_skills.append(skill)

    # Detect synonyms
    for synonym, actual_skill in synonyms.items():

        pattern = r"\b" + re.escape(synonym) + r"\b"

        if re.search(pattern, text):
            found_skills.append(actual_skill)

    return sorted(list(set(found_skills)))