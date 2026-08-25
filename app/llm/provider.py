import json
import logging
import os
import re
from typing import Optional

from openai import AsyncClient
from pydantic import ValidationError

from pipeline.validator import ProductListSchema

logger = logging.getLogger(__name__)

class LLMProvider:
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: Optional[str] = None,
        timeout: float = 60.0,
    ) -> None:
        resolved_api_key = (
            api_key
            or os.getenv("DEEPSEEK_API_KEY")
            or os.getenv("QWEN_API_KEY")
        )
        if not resolved_api_key:
            raise ValueError("API key is required. Set DEEPSEEK_API_KEY in .env")

        self.client = AsyncClient(
            api_key=resolved_api_key,
            base_url=base_url or os.getenv("LLM_BASE_URL", "https://openrouter.ai/api/v1"),
            timeout=timeout,
        )
        self.model = model or os.getenv("LLM_MODEL", "openrouter/free")

    async def extract_product(self, raw_text: str) -> ProductListSchema:
        truncated_text = raw_text[:3500]

        prompt = (
            "You are a structured data extractor. Extract exactly 5 laptop products from the text below.\n"
            "Respond ONLY with a raw JSON object matching this schema:\n"
            "{\n"
            '  "products": [\n'
            '    {"title": "string", "price": 0.0, "description": "string", "url": "string"}\n'
            "  ]\n"
            "}\n"
            "Extract actual data from the text. Do NOT add explanations or think tags.\n\n"
            f"Content:\n{truncated_text}"
        )

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=2000,
            )
        except Exception as exc:
            raise RuntimeError(f"LLM API call failed: {exc}") from exc

        message = response.choices[0].message
        msg_dict = message.model_dump()
        
        # Smart fallback for models that output data within reasoning fields
        content = message.content or msg_dict.get("reasoning") or ""

        if not content:
            raise ValueError("LLM returned empty content and empty reasoning field.")

        # Clean up potential reasoning tags before JSON parsing
        cleaned_content = re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL).strip()
        
        start_idx = cleaned_content.find('{"products"')
        if start_idx == -1:
            start_idx = cleaned_content.find('{')

        if start_idx == -1:
            raise ValueError("No JSON object found in the LLM output.")

        decoder = json.JSONDecoder()
        try:
            data, _ = decoder.raw_decode(cleaned_content[start_idx:])
            return ProductListSchema.model_validate(data)
        except Exception as exc:
            logger.error(f"Failed to parse JSON. Raw LLM content snippet: {content[:200]}")
            raise ValueError(f"Failed to parse JSON: {exc}") from exc

_provider: Optional[LLMProvider] = None

def get_provider() -> LLMProvider:
    global _provider
    if _provider is None:
        _provider = LLMProvider()
    return _provider

async def extract_product(raw_text: str) -> ProductListSchema:
    provider = get_provider()
    return await provider.extract_product(raw_text)