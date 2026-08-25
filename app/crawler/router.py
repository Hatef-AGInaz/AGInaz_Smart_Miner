import logging
from typing import Dict, Any
import httpx
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

logger = logging.getLogger(__name__)

async def fetch_static(url: str) -> str:
    print(f"[httpx] Fetching static content from {url}")
    async with httpx.AsyncClient(verify=False) as client:
        response = await client.get(url, timeout=15.0)
        response.raise_for_status()
        print(f"HTTP Request: GET {url} \"HTTP/{response.http_version} {response.status_code}\"")
        soup = BeautifulSoup(response.text, "html.parser")
        return soup.get_text(separator=" ", strip=True)

async def fetch_dynamic(url: str) -> str:
    print(f"[playwright] Launching local Chrome for {url}")
    async with async_playwright() as p:
        # Launching the system's local Chrome with evasion arguments
        browser = await p.chromium.launch(
            headless=True,
            channel="chrome",
            args=["--disable-blink-features=AutomationControlled"]
        )
        context = await browser.new_context()
        page = await context.new_page()
        print(f"[playwright] Navigating to {url}")
        
        # Graceful timeout mechanism for heavy dynamic content
        await page.goto(url, wait_until="networkidle", timeout=30000)
        content = await page.content()
        await browser.close()
        
        soup = BeautifulSoup(content, "html.parser")
        return soup.get_text(separator=" ", strip=True)

async def route(url: str, min_text_length: int = 600) -> Dict[str, Any]:
    print(f"[router] Starting routing for {url}")
    try:
        # Step 1: Attempt fast static fetch
        text = await fetch_static(url)
        
        # Step 2: Evaluate content viability
        if len(text) >= min_text_length:
            print(f"[router] Static fetch successful and sufficient for {url}")
            return {"success": True, "text": text}
        
        print(f"[router] Static content insufficient for {url}: Text length ({len(text)}) is below minimum ({min_text_length}). Falling back to Playwright.")
        
        # Step 3: Execute dynamic rendering fallback
        text = await fetch_dynamic(url)
        return {"success": True, "text": text}
        
    except Exception as e:
        logger.error(f"[router] Routing execution failed for {url}: {e}")
        return {"success": False, "error": str(e), "text": ""}