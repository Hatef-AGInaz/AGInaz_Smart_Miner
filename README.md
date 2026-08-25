# AGInaz Smart Miner 🚀

Intelligent Web Extraction Pipeline — From Unstructured Websites to Validated, Machine-Ready Data

AGInaz Smart Miner is a production-ready intelligent web extraction pipeline designed to turn messy, unstructured web content into clean, structured data automatically.

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

## 🚀 Current Status & Roadmap

Version v1.0  Status Production-Ready MVP
The current release represents a complete end-to-end extraction workflow. The repository has been intentionally minimized and cleaned to present the project as a focused, professional engineering product.

### v2.0 — Advanced Web Intelligence (Coming Soon)
 Advanced anti-bot environments & Cloudflare-aware strategies
 Complex authentication workflows (Multi-step logins)
 Direct integration with Vector Databases & Knowledge Graph pipelines
 RAG-ready data generation for AI Agents

---
Built as the second project in the AGInaz three-project engineering portfolio.