# 🛠️ AGInaz Smart Miner — Setup & Quickstart

Technical setup guide for AGInaz Smart Miner v1.0. This document covers the required environment, dependency installation, configuration, and application startup.

## 1. Prerequisites

Before running the project, make sure the following are installed:
* Python 3.10+
* `pip`
* Git
* Google Chrome or Chromium (recommended for Playwright-based extraction)
* An OpenRouter-compatible LLM API key

Verify Python and pip:
python --version
pip --version

## 2. Clone the Repository

Clone the project and enter its directory:
git clone https://github.com/Hatef-AGInaz/AGInaz_Smart_Miner.git
cd AGInaz_Smart_Miner

## 3. Install Python Dependencies

Install the project's required Python packages:
pip install -r requirements.txt

## 4. Install Playwright Chromium

Smart Miner uses Playwright as its browser-based fallback for JavaScript-heavy websites. Install the required Chromium browser:
playwright install chromium

## 5. Configure Environment Variables

Create a `.env` file in the project root:
DEEPSEEK_API_KEY=your_api_key_here
LLM_BASE_URL=https://openrouter.ai/api/v1
LLM_MODEL=your_model_name_here

*(Never commit `.env` or API credentials to GitHub. Make sure `.env` is included in `.gitignore`.)*

## 6. Run Smart Miner

From the project root, start the application with:
python app/main.py

The application will initialize the extraction pipeline and use the configured environment variables for LLM communication. 

## 7. Troubleshooting

* **Playwright Browser Not Found:** Run `playwright install chromium` then retry.
* **Missing API Configuration:** Verify that `.env` exists in the project root and contains the correct keys.