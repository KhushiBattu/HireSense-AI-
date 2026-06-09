import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Load dataset
df = pd.read_csv("data/roles.csv")

# Vectorization
vectorizer = TfidfVectorizer()

X = vectorizer.fit_transform(df["skills"])

# Model Training
model = LogisticRegression(max_iter=1000)

model.fit(X, df["role"])


def filter_role_skills(skills):

    important_skills = [
        "Machine Learning",
        "Deep Learning",
        "NLP",
        "Data Science",
        "Scikit-Learn",
        "TensorFlow",
        "PyTorch",
        "NumPy",
        "Pandas",
        "Computer Vision",
        "Generative AI",
        "Transformers",
        "LLM"
    ]

    filtered = []

    for skill in skills:
        if skill in important_skills:
            filtered.append(skill)

    return filtered


def predict_role(skills):

    text = " ".join(skills)

    X_test = vectorizer.transform([text])

    prediction = model.predict(X_test)[0]

    probabilities = model.predict_proba(X_test)[0]

    confidence = round(max(probabilities) * 100, 2)

    classes = model.classes_

    role_scores = []

    for role, prob in zip(classes, probabilities):
        role_scores.append(
            (role, round(prob * 100, 2))
        )

    role_scores.sort(
        key=lambda x: x[1],
        reverse=True
    )

    return prediction, confidence, role_scores[:3]