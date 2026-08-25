import asyncio
import csv
import logging
import os
from dotenv import load_dotenv

load_dotenv(override=True)

from crawler.router import route
from llm.provider import extract_product

logging.basicConfig(level=logging.INFO, format="%(message)s")

async def main():
    print("🚀 Starting AGInaz Smart Miner (Dynamic Extraction Engine)...\n")

    url = "https://webscraper.io/test-sites/e-commerce/ajax/computers/laptops"
    print(f"🎯 Target URL: {url}")

    # Routing threshold: pages under 600 chars will trigger Playwright (Dynamic rendering)
    result = await route(url, min_text_length=600)

    if not result["success"]:
        print(f"❌ Crawler failed: {result.get('error', 'Unknown error')}")
        return

    raw_text = result["text"]
    print(f"✅ Content Extracted Successfully ({len(raw_text)} characters).")
    print("🧠 Processing with AI Extraction Engine...")

    try:
        structured_data = await extract_product(raw_text)
        print("\n✨ Data Extraction Completed Successfully! ✨\n")

        output_dir = "outputs"
        os.makedirs(output_dir, exist_ok=True)
        csv_filepath = os.path.join(output_dir, "extracted_products.csv")

        with open(csv_filepath, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Title", "Price", "Description", "URL"])

            for p in structured_data.products:
                writer.writerow([p.title, p.price, p.description, p.url])
                print(f"💻 {p.title[:45]}... | 💲{p.price}")

        print(f"\n✅ Success! File saved to '{csv_filepath}'.")
    except Exception as e:
        print(f"\n❌ AI Processing Failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())