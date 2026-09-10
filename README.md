# AGInaz Smart Miner 🚀

Standalone, reusable web extraction engine — from unstructured websites to
validated, machine-ready data.

AGInaz Smart Miner v1.2.0 is a production-ready extraction engine designed to
turn messy web content into clean data for downstream AI agents, research
systems, ETL pipelines, and other software projects. It can run as a standalone
engine; it is not tied to a UI or to the bundled product-extraction example.

## 🤔 Why Smart Miner

Modern websites are not equally difficult to scrape. Some can be extracted with a simple HTTP request in milliseconds. Others depend heavily on JavaScript, AJAX requests, dynamic rendering, or browser execution.

Using a browser for everything is expensive and slow. Using HTTP for everything simply fails.
Smart Miner chooses the right extraction strategy automatically.

Target Website → Smart Router → HTTPX  Playwright → Raw Data → LLM → JSON → Pydantic → CSV

## 💎 Core Value Proposition

 Speed First — Static pages are processed through `httpx`, avoiding unnecessary browser overhead.
 Intelligent Routing — The pipeline evaluates extracted content and automatically determines when browser rendering is necessary.
 JavaScript-Aware Extraction — When a website depends on JavaScript or AJAX rendering, Smart Miner falls back to `Playwright` with a local ChromeChromium instance.
 LLM-Powered Structuring — Raw web content is transformed into structured records using an LLM rather than relying exclusively on brittle CSS selectors.
 Reliable JSON Output — Providermodel behavior is normalized to prevent reasoning artifacts such as `think` blocks from contaminating structured output.
 Strict Data Validation — `Pydantic` validates the final schema before data reaches the export layer.

## 🏗️ Hybrid Architecture

### Layer 1 — HTTP Extraction
`httpx` handles websites that expose their content directly through standard HTTP responses. This provides extremely low overhead, high throughput, minimal resource consumption, and fast execution.

### Layer 2 — Intelligent Browser Fallback
When the initial response contains insufficient meaningful content, the router treats the target as potentially JavaScript-dependent. `Playwright` then launches a local ChromiumChrome environment to execute the page and retrieve dynamically rendered content. Browser automation is used when necessary — not by default.

### LLM Extraction Layer
Once raw content has been collected, Smart Miner delegates semantic extraction to an LLM. Instead of hard-coding every possible HTML structure, the system can interpret page content and map it into a predefined data schema.

## ⚙️ Technology Stack

 Component  Role 
-----------------
 Python  Core application 
 httpx  High-speed HTTP extraction 
 Playwright  Dynamic browser-based extraction 
 Chromium  JavaScript execution environment 
 OpenRouter  LLM gateway 
 DeepSeek  Qwen  Semantic extraction 
 Pydantic  Schema validation 
 CSV  Structured export 

## 🚦 Version 1.2.0 — Explainable Smart Routing

**Status: Current release (v1.2.0)**

The router now evaluates static content using deterministic visible-character,
word-count, and text-diversity signals. It uses Playwright only when one or more
quality checks fail and reports stable reason codes for that decision.

`route()` remains compatible with existing consumers: `success`, `text`, and
`error` are always present. Routing details are returned separately under
`routing`:

```python
{
    "success": True,
    "text": "extracted visible text",
    "error": None,
    "routing": {
        "strategy": "static",  # static, dynamic, or failed
        "fallback_used": False,
        "reason_codes": ["STATIC_QUALITY_ACCEPTED"],
        "visible_character_count": 1234,
        "timing_ms": {"static": 18.2, "dynamic": 0.0, "total": 18.3},
    },
}
```

Fallback reason codes are `INSUFFICIENT_VISIBLE_TEXT`,
`INSUFFICIENT_WORD_COUNT`, and `LOW_TEXT_DIVERSITY`. Failures use
`ROUTING_ERROR`.

Run the isolated unit tests (no live website access) with:

```bash
python -m unittest discover -v
```

## Changelog

### v1.2.0

- Replaced the single length threshold with deterministic content-quality checks.
- Added strategy, fallback, reason-code, visible-character, and timing metadata.
- Preserved the existing `success`, `text`, and `error` response keys.
- Added mocked HTTPX and Playwright unit tests.

### v1.1

- Refactored the project into a reusable extraction engine.
- Added redirect handling and Windows UTF-8 output support.

## Previous release: v1.1 — The Engine Update

**Status: Historical release**

In version 1.1, AGInaz Smart Miner has been heavily refactored to act as a **standalone extraction engine** for other AI systems (such as the *DePIN Research Agent*). 

### Key Updates in v1.1:
- **Engine-Ready Architecture:** Designed to seamlessly feed extracted, structured text/data directly into downstream AI pipelines.
- **Reusable for Other Projects:** This smart miner is a highly modular tool that can be easily adapted and is extremely useful for other data extraction and AI projects.
- **Robust Redirection Handling:** Seamlessly follows HTTP 301/302 redirects without dropping extraction tasks.
- **Cross-Platform Stability:** Added native Windows UTF-8 encoding support to prevent terminal crashes when handling complex characters and emojis.
- **Internationalization:** The entire codebase, including inline documentation and terminal outputs, has been standardized to English for global open-source adoption.

### v2.0 — Advanced Web Intelligence (Coming Soon)
- Advanced anti-bot environments & Cloudflare-aware strategies
- Complex authentication workflows (Multi-step logins)
- Direct integration with Vector Databases & Knowledge Graph pipelines
- RAG-ready data generation for AI Agents

---
*Built as the foundational extraction engine in the AGInaz engineering portfolio.*

