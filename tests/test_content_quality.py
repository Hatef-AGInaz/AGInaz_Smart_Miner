import unittest

from examples.content_quality import evaluate_content_quality


class ContentQualityTests(unittest.TestCase):
    def test_distinct_long_content_is_accepted(self):
        text = " ".join(f"project-{number}" for number in range(80))
        result = evaluate_content_quality(text)
        self.assertTrue(result["accepted"])
        self.assertEqual(result["reason_codes"], [])

    def test_long_but_repetitive_content_needs_fallback(self):
        result = evaluate_content_quality("token " * 120)
        self.assertEqual(result["reason_codes"], ["LOW_TEXT_DIVERSITY"])

    def test_short_content_explains_both_missing_signals(self):
        result = evaluate_content_quality("Loading")
        self.assertEqual(result["reason_codes"], [
            "INSUFFICIENT_VISIBLE_TEXT", "INSUFFICIENT_WORD_COUNT"
        ])

    def test_negative_threshold_rejected(self):
        with self.assertRaises(ValueError):
            evaluate_content_quality("content", -1)


if __name__ == "__main__":
    unittest.main()
