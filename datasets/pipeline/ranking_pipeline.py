def rank_response(
    response,
    educational_score,
    clarity_score,
    safety_score
):

    final_score = (
        educational_score * 0.5 + clarity_score * 0.3 + safety_score * 0.2
    )

    return round(
        final_score,
        2
    )