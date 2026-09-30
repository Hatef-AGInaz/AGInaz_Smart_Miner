# AGInaz Smart Miner

**Turn messy web pages into reusable, structured documents for research workflows.**

![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?style=flat-square&logo=python&logoColor=white)
![HTTPX](https://img.shields.io/badge/HTTPX-HTTP_fetch-3B82F6?style=flat-square)
![Playwright](https://img.shields.io/badge/Playwright-browser_fallback-2EAD33?style=flat-square&logo=playwright&logoColor=white)
![Beautiful Soup](https://img.shields.io/badge/Beautiful_Soup-HTML_parsing-8B5CF6?style=flat-square)
![Markdownify](https://img.shields.io/badge/Markdownify-structured_text-475569?style=flat-square)
![Pydantic](https://img.shields.io/badge/Pydantic-schema_validation-E92063?style=flat-square&logo=pydantic&logoColor=white)

Smart Miner first tries a lightweight HTTP fetch. If the visible content is too
short or repetitive, it can render the page in a browser. A local cleaner then
keeps useful structure—headings, tables, links, source URL and valid JSON-LD—
in a document that can be reused for later extraction.

**This is the public portfolio view.** The full engine is developed privately.
This repository contains one small, testable routing excerpt from v1.2 and a
recorded example using synthetic data. It is not a downloadable engine build.

## Take a quick look

| If you want to see… | Open |
| --- | --- |
| What a messy page becomes | [Before/after example](examples/sample-output.md) |
| A visual walkthrough | [Local HTML demo](demo/index.html) |
| A slice of the implementation | [Content-quality signal](examples/content_quality.py) and [tests](tests/test_content_quality.py) |

The HTML demo is a static page you can open locally. It displays a recorded
output; it does not fetch a website or invoke an LLM.

## How the engine works

```text
URL → HTTPX → visible-content quality check ── sufficient ──┐
                     └─ insufficient → Playwright ────────────┤
                                                              ↓
                                  barrier check → local cleaner
                                                        ↓
                                  reusable CleanDocument
                                                        ↓ optional
                                  model extraction → Pydantic
```

- The browser path has a bounded wait for dynamic content. It is used only when
  the static-content checks call for it.
- Cleaning preserves headings, tables and resolved links. Valid JSON-LD is
  retained as source data. Identical navigation blocks can be deduplicated;
  repeated data rows remain.
- Challenge/CAPTCHA signals stop processing before optional model extraction.
  Detection is heuristic and does not solve CAPTCHA.
- Pydantic validates an output's structure and types. It cannot establish
  whether the extracted claims are true.

The existing v1.2 `route()` response keeps `success`, `text`, `error`, and its
`routing` metadata. The newer local pipeline adds a reusable document and a
clear status for blocked pages.

## Evidence, with limits

The local prototype passed **19 offline tests** and **one opt-in browser test**
using a delayed AJAX page served from a loopback server. The public routing
excerpt has [four independent tests](tests/test_content_quality.py):

```bash
python -m unittest discover -v
```

For the synthetic page, raw HTML measured **473 characters** and the complete
clean extraction input measured **309 characters** (including source URL and
title). That is one fixture, measured in characters—not a token-cost benchmark
or a claimed saving across websites.

The demonstrated scope is single-page fetching, cleaning, barrier stopping
and optional extraction. It does not include login recovery, CAPTCHA solving,
large-scale crawling or multi-agent orchestration.

## What is public

This portfolio repository contains the README, a static HTML walkthrough, a
recorded synthetic output, and a small v1.2 routing-signal excerpt with tests.
It has a fresh Git history, separate from the engine repository. The fetcher,
cleaner, orchestrator, browser control and LLM provider are **not included**.

A Streamlit version is being reviewed locally. We will inspect and test its UI
before deciding whether to publish it, and only then add a live-demo link here.
This engine portfolio does not need a GitHub Release; the repository and demo
are the presentation.

**Project:** AGInaz · **Private development target:** v1.3.0
