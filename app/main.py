import asyncio
import os
import sys
import logging

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding.lower() != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

from crawler.router import route

logging.basicConfig(level=logging.INFO, format="%(message)s")

async def main():
    print("🚀 Starting AGInaz Smart Miner Engine (Extraction Only)...\n")

    # Sample test URL (e.g., Grass project used in DePIN tests)
    url = "https://getgrass.io/"
    print(f"🎯 Target URL: {url}")

    # Fallback to Playwright if text length is less than 600 characters
    result = await route(url, min_text_length=600)

    if not result["success"]:
        print(f"❌ Crawler failed: {result.get('error', 'Unknown error')}")
        return

    raw_text = result["text"]
    print(f"✅ Content Extracted Successfully ({len(raw_text)} characters).")

    # Save raw extracted text to inspect output quality
    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)
    text_filepath = os.path.join(output_dir, "extracted_raw.txt")

    with open(text_filepath, "w", encoding="utf-8") as f:
        f.write(raw_text)

    print(f"💾 Raw extracted text saved to '{text_filepath}'.")
    print("✅ Ready to be consumed by Project 3 (DePIN Agent)!")

if __name__ == "__main__":
    asyncio.run(main())