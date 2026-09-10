import unittest
from unittest.mock import AsyncMock, MagicMock, patch

from app.crawler.router import (
    evaluate_content_quality,
    fetch_dynamic,
    fetch_static,
    route,
)


class ContentQualityTests(unittest.TestCase):
    def test_long_repetitive_content_is_rejected(self):
        quality = evaluate_content_quality("token " * 120, min_text_length=600)

        self.assertFalse(quality["accepted"])
        self.assertEqual(quality["reason_codes"], ["LOW_TEXT_DIVERSITY"])


class FetchTests(unittest.IsolatedAsyncioTestCase):
    @patch("app.crawler.router.httpx")
    async def test_fetch_static_uses_mocked_httpx_and_removes_non_visible_tags(
        self, httpx_mock
    ):
        response = MagicMock(
            text="<main>Hello <b>world</b></main><script>hidden()</script>",
            http_version="1.1",
            status_code=200,
        )
        client = AsyncMock()
        client.get.return_value = response
        httpx_mock.AsyncClient.return_value.__aenter__ = AsyncMock(return_value=client)
        httpx_mock.AsyncClient.return_value.__aexit__ = AsyncMock(return_value=None)

        text = await fetch_static("https://example.test")

        self.assertEqual(text, "Hello world")
        client.get.assert_awaited_once_with("https://example.test", timeout=15.0)
        response.raise_for_status.assert_called_once_with()
        httpx_mock.AsyncClient.assert_called_once_with(
            verify=False, follow_redirects=True
        )

    @patch("app.crawler.router.async_playwright")
    async def test_fetch_dynamic_uses_mocked_playwright(self, async_playwright_mock):
        page = AsyncMock()
        page.content.return_value = "<article>Rendered content</article><style>x{}</style>"
        context = AsyncMock()
        context.new_page.return_value = page
        browser = AsyncMock()
        browser.new_context.return_value = context
        playwright = MagicMock()
        playwright.chromium.launch = AsyncMock(return_value=browser)
        manager = MagicMock()
        manager.__aenter__ = AsyncMock(return_value=playwright)
        manager.__aexit__ = AsyncMock(return_value=None)
        async_playwright_mock.return_value = manager

        text = await fetch_dynamic("https://example.test")

        self.assertEqual(text, "Rendered content")
        playwright.chromium.launch.assert_awaited_once_with(
            headless=True, channel="chrome"
        )
        page.goto.assert_awaited_once_with(
            "https://example.test", wait_until="networkidle", timeout=30000
        )
        browser.close.assert_awaited_once_with()


class RoutingTests(unittest.IsolatedAsyncioTestCase):
    @patch("app.crawler.router.fetch_dynamic", new_callable=AsyncMock)
    @patch("app.crawler.router.fetch_static", new_callable=AsyncMock)
    async def test_accepts_high_quality_static_content(
        self, fetch_static_mock, fetch_dynamic_mock
    ):
        static_text = " ".join(f"useful-word-{index}" for index in range(80))
        fetch_static_mock.return_value = static_text

        result = await route("https://example.test", min_text_length=600)

        self.assertTrue(result["success"])
        self.assertEqual(result["text"], static_text)
        self.assertIsNone(result["error"])
        self.assertEqual(result["routing"]["strategy"], "static")
        self.assertFalse(result["routing"]["fallback_used"])
        self.assertEqual(
            result["routing"]["reason_codes"], ["STATIC_QUALITY_ACCEPTED"]
        )
        self.assertEqual(
            result["routing"]["visible_character_count"], len(static_text)
        )
        self.assertGreaterEqual(result["routing"]["timing_ms"]["total"], 0)
        fetch_dynamic_mock.assert_not_awaited()

    @patch("app.crawler.router.fetch_dynamic", new_callable=AsyncMock)
    @patch("app.crawler.router.fetch_static", new_callable=AsyncMock)
    async def test_short_static_content_falls_back_to_dynamic(
        self, fetch_static_mock, fetch_dynamic_mock
    ):
        fetch_static_mock.return_value = "Too short"
        fetch_dynamic_mock.return_value = "Rendered page content"

        result = await route("https://example.test", min_text_length=600)

        self.assertTrue(result["success"])
        self.assertEqual(result["text"], "Rendered page content")
        self.assertEqual(result["routing"]["strategy"], "dynamic")
        self.assertTrue(result["routing"]["fallback_used"])
        self.assertEqual(
            result["routing"]["reason_codes"],
            ["INSUFFICIENT_VISIBLE_TEXT", "INSUFFICIENT_WORD_COUNT"],
        )
        self.assertEqual(result["routing"]["visible_character_count"], 21)

    @patch("app.crawler.router.fetch_dynamic", new_callable=AsyncMock)
    @patch("app.crawler.router.fetch_static", new_callable=AsyncMock)
    async def test_long_low_diversity_content_falls_back(
        self, fetch_static_mock, fetch_dynamic_mock
    ):
        fetch_static_mock.return_value = "token " * 120
        fetch_dynamic_mock.return_value = "Rendered"

        result = await route("https://example.test", min_text_length=600)

        self.assertEqual(result["routing"]["strategy"], "dynamic")
        self.assertEqual(
            result["routing"]["reason_codes"], ["LOW_TEXT_DIVERSITY"]
        )
        fetch_dynamic_mock.assert_awaited_once_with("https://example.test")

    @patch("app.crawler.router.fetch_static", new_callable=AsyncMock)
    async def test_error_preserves_compatibility_keys_and_failure_metadata(
        self, fetch_static_mock
    ):
        fetch_static_mock.side_effect = RuntimeError("network unavailable")

        result = await route("https://example.test")

        self.assertFalse(result["success"])
        self.assertEqual(result["text"], "")
        self.assertEqual(result["error"], "network unavailable")
        self.assertEqual(result["routing"]["strategy"], "failed")
        self.assertFalse(result["routing"]["fallback_used"])
        self.assertEqual(result["routing"]["reason_codes"], ["ROUTING_ERROR"])

    @patch("app.crawler.router.fetch_dynamic", new_callable=AsyncMock)
    @patch("app.crawler.router.fetch_static", new_callable=AsyncMock)
    async def test_dynamic_error_reports_attempted_fallback(
        self, fetch_static_mock, fetch_dynamic_mock
    ):
        fetch_static_mock.return_value = "Too short"
        fetch_dynamic_mock.side_effect = RuntimeError("browser unavailable")

        result = await route("https://example.test", min_text_length=600)

        self.assertFalse(result["success"])
        self.assertEqual(result["error"], "browser unavailable")
        self.assertTrue(result["routing"]["fallback_used"])
        self.assertGreaterEqual(result["routing"]["timing_ms"]["dynamic"], 0)


if __name__ == "__main__":
    unittest.main()

