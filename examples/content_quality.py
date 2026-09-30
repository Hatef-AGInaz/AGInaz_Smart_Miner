"""Public v1.2 excerpt: explainable static-page quality signals.

This small, dependency-free example illustrates a routing decision. It is
not the private fetcher, cleaner, browser controller or extraction pipeline.
"""
import re


def evaluate_content_quality(text: str, min_text_length: int = 600) -> dict:
    if min_text_length < 0:
        raise ValueError("min_text_length must be non-negative")

    visible_character_count = len(text.strip())
    words = re.findall(r"\b[\w'-]+\b", text.casefold(), flags=re.UNICODE)
    word_count = len(words)
    unique_word_ratio = len(set(words)) / word_count if word_count else 0.0
    minimum_word_count = max(1, min_text_length // 12) if min_text_length else 0

    reason_codes = []
    if visible_character_count < min_text_length:
        reason_codes.append("INSUFFICIENT_VISIBLE_TEXT")
    if word_count < minimum_word_count:
        reason_codes.append("INSUFFICIENT_WORD_COUNT")
    if word_count >= 20 and unique_word_ratio < 0.2:
        reason_codes.append("LOW_TEXT_DIVERSITY")

    return {
        "accepted": not reason_codes,
        "reason_codes": reason_codes,
        "visible_character_count": visible_character_count,
        "word_count": word_count,
        "unique_word_ratio": round(unique_word_ratio, 4),
    }
