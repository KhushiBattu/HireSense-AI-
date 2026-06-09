def calculate_ats_score(matched, missing, related):

    exact_matches = len(matched)

    related_matches = len(related)

    total_required = (
        len(matched)
        + len(missing)
    )

    if total_required == 0:
        return 0

    score = (
        (
            exact_matches
            + (0.75 * related_matches)
        )
        /
        total_required
    ) * 100

    # small baseline boost
    score += 10

    return min(round(score), 100)