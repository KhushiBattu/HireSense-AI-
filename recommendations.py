def get_recommendations(skills):

    recommendations = []

    skill_set = [skill.lower() for skill in skills]

    if "aws" not in skill_set:
        recommendations.append(
            "Learn AWS or Cloud Computing fundamentals."
        )

    if "docker" not in skill_set:
        recommendations.append(
            "Gain experience with Docker and deployment tools."
        )

    if (
        "deep learning" in skill_set
        and "tensorflow" not in skill_set
        and "pytorch" not in skill_set
    ):
        recommendations.append(
            "Gain hands-on experience with TensorFlow or PyTorch."
        )

    return recommendations