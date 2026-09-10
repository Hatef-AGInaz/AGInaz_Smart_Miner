import logging
import re
from html.parser import HTMLParser
from time import perf_counter
from typing import Any, Dict, List, Optional

try:
    import httpx
except ModuleNotFoundError:  # Allows dependency-free unit-test collection.
    httpx = None

try:
    from bs4 import BeautifulSoup
except ModuleNotFoundError:  # The standard-library parser below is the fallback.
    BeautifulSoup = None

try:
    from playwright.async_api import async_playwright
except ModuleNotFoundError:  # Tests replace this symbol with a mock.
    async_playwright = None

logger = logging.getLogger(__name__)

LOW_TEXT_DIVERSITY_THRESHOLD = 0.2
MIN_WORDS_FOR_DIVERSITY_CHECK = 20


class _VisibleTextParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._hidden_depth = 0
        self.parts: List[str] = []

    def handle_starttag(self, tag: str, attrs: List[Any]) -> None:
        if tag in {"script", "style", "noscript"}:
            self._hidden_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style", "noscript"} and self._hidden_depth:
            self._hidden_depth -= 1

    def handle_data(self, data: str) -> None:
        if not self._hidden_depth and data.strip():
            self.parts.append(data)


def _extract_visible_text(html: str) -> str:
    if BeautifulSoup is not None:
        soup = BeautifulSoup(html, "html.parser")
        for tag in soup(["script", "style", "noscript"]):
            tag.extract()
        return soup.get_text(separator=" ", strip=True)

    parser = _VisibleTextParser()
    parser.feed(html)
    return " ".join(" ".join(parser.parts).split())


def evaluate_content_quality(text: str, min_text_length: int = 600) -> Dict[str, Any]:
    """Return deterministic quality signals used by the routing decision."""
    if min_text_length < 0:
        raise ValueError("min_text_length must be non-negative")

    visible_character_count = len(text.strip())
    words = re.findall(r"\b[\w'-]+\b", text.casefold(), flags=re.UNICODE)
    word_count = len(words)
    unique_word_ratio = len(set(words)) / word_count if word_count else 0.0
    minimum_word_count = max(1, min_text_length // 12) if min_text_length else 0

    reason_codes: List[str] = []
    if visible_character_count < min_text_length:
        reason_codes.append("INSUFFICIENT_VISIBLE_TEXT")
    if word_count < minimum_word_count:
        reason_codes.append("INSUFFICIENT_WORD_COUNT")
    if (
        word_count >= MIN_WORDS_FOR_DIVERSITY_CHECK
        and unique_word_ratio < LOW_TEXT_DIVERSITY_THRESHOLD
    ):
        reason_codes.append("LOW_TEXT_DIVERSITY")

    return {
        "accepted": not reason_codes,
        "reason_codes": reason_codes,
        "visible_character_count": visible_character_count,
        "word_count": word_count,
        "unique_word_ratio": round(unique_word_ratio, 4),
    }


async def fetch_static(url: str) -> str:
    if httpx is None:
        raise RuntimeError("httpx is required for static extraction")
    print(f"[httpx] Fetching static content from {url}")
    async with httpx.AsyncClient(verify=False, follow_redirects=True) as client:
        response = await client.get(url, timeout=15.0)
        response.raise_for_status()
        print(
            f'HTTP Request: GET {url} '
            f'"HTTP/{response.http_version} {response.status_code}"'
        )
        return _extract_visible_text(response.text)


async def fetch_dynamic(url: str) -> str:
    if async_playwright is None:
        raise RuntimeError("playwright is required for dynamic extraction")
    print(f"[playwright] Launching local Chrome for {url}")
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True, channel="chrome")
        try:
            context = await browser.new_context()
            page = await context.new_page()
            print(f"[playwright] Navigating to {url}")
            await page.goto(url, wait_until="networkidle", timeout=30000)
            content = await page.content()
        finally:
            await browser.close()

    return _extract_visible_text(content)


def _elapsed_ms(started_at: float) -> float:
    return round((perf_counter() - started_at) * 1000, 2)


async def route(url: str, min_text_length: int = 600) -> Dict[str, Any]:
    """Extract a URL and return compatible content plus explainable routing data."""
    print(f"[router] Starting routing for {url}")
    route_started_at = perf_counter()
    static_started_at = perf_counter()
    static_ms = 0.0
    dynamic_ms = 0.0
    dynamic_started_at: Optional[float] = None
    fallback_used = False

    try:
        text = await fetch_static(url)
        static_ms = _elapsed_ms(static_started_at)
        quality = evaluate_content_quality(text, min_text_length)

        if quality["accepted"]:
            print(f"[router] Static fetch successful and sufficient for {url}")
            return {
                "success": True,
                "text": text,
                "error": None,
                "routing": {
                    "strategy": "static",
                    "fallback_used": False,
                    "reason_codes": ["STATIC_QUALITY_ACCEPTED"],
                    "visible_character_count": quality["visible_character_count"],
                    "timing_ms": {
                        "static": static_ms,
                        "dynamic": dynamic_ms,
                        "total": _elapsed_ms(route_started_at),
                    },
                },
            }

        fallback_used = True
        reasons = ", ".join(quality["reason_codes"])
        print(
            f"[router] Static content quality insufficient for {url}: {reasons}. "
            "Falling back to Playwright."
        )
        dynamic_started_at = perf_counter()
        text = await fetch_dynamic(url)
        dynamic_ms = _elapsed_ms(dynamic_started_at)
        return {
            "success": True,
            "text": text,
            "error": None,
            "routing": {
                "strategy": "dynamic",
                "fallback_used": True,
                "reason_codes": quality["reason_codes"],
                "visible_character_count": len(text.strip()),
                "timing_ms": {
                    "static": static_ms,
                    "dynamic": dynamic_ms,
                    "total": _elapsed_ms(route_started_at),
                },
            },
        }
    except Exception as exc:
        if not static_ms:
            static_ms = _elapsed_ms(static_started_at)
        if dynamic_started_at is not None and not dynamic_ms:
            dynamic_ms = _elapsed_ms(dynamic_started_at)
        logger.error(f"[router] Routing execution failed for {url}: {exc}")
        return {
            "success": False,
            "error": str(exc),
            "text": "",
            "routing": {
                "strategy": "failed",
                "fallback_used": fallback_used,
                "reason_codes": ["ROUTING_ERROR"],
                "visible_character_count": 0,
                "timing_ms": {
                    "static": static_ms,
                    "dynamic": dynamic_ms,
                    "total": _elapsed_ms(route_started_at),
                },
            },
        }

