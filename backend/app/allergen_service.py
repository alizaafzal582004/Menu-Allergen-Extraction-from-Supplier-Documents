import os
import json
import time
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)


def detect_allergens(extracted_text: str) -> dict:
    """
    Takes extracted document text (from MinerU) and returns a dictionary
    of detected ingredients and allergens, using Qwen via OpenRouter.
    """
    prompt = f"""You are a food safety allergen classification expert. You will be given text extracted from a supplier's product specification sheet, which may be in Catalan, Spanish, or English.

Your task:
1. Identify every ingredient listed.
2. For each ingredient, determine if it corresponds to one of the 14 EU Annex II major allergens (cereals containing gluten, crustaceans, eggs, fish, peanuts, soybeans, milk, tree nuts, celery, mustard, sesame, sulphur dioxide/sulphites, lupin, molluscs).
3. Include allergens that are explicitly stated in the document AND allergens you infer from ingredient names even if not explicitly stated.
4. For each allergen, set "detection_method" to "explicit_statement" ONLY if the document contains a direct statement like "Contains: X" or "May contain traces of X". If the allergen is only implied by an ingredient's name, always use "inferred" — even if the ingredient name itself is a well-known/obvious translation.
5. Be careful: some ingredient names contain misleading words (e.g. "nou moscada" means nutmeg, a spice — NOT a tree nut, even though "nou" alone means walnut). Do not falsely flag ingredients based on partial word matches.
6. If you are not confident about an ingredient, mark it as "needs_human_review": true rather than guessing.

Respond ONLY with valid JSON in this exact structure, no other text:

{{
  "ingredients": ["list", "of", "all", "ingredients", "found"],
  "allergens_detected": [
    {{
      "allergen": "allergen name",
      "source_ingredient": "ingredient that triggered detection",
      "detection_method": "explicit_statement or inferred",
      "confidence": "high or medium or low",
      "needs_human_review": false
    }}
  ]
}}

Document text:
{extracted_text}
"""

    response = client.chat.completions.create(
        model="qwen/qwen-2.5-72b-instruct",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1500,
    )

    result_text = response.choices[0].message.content

    cleaned = result_text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("```")[1]
        if cleaned.startswith("json"):
            cleaned = cleaned[4:]

    try:
        parsed_result = json.loads(cleaned)
    except json.JSONDecodeError:
        raise ValueError(f"Qwen did not return valid JSON. Raw output: {result_text}")

    return parsed_result


def detect_allergens_with_retry(extracted_text: str, max_retries: int = 3, delay_seconds: int = 15) -> dict:
    """
    Wraps detect_allergens() with automatic retries, since free-tier OpenRouter
    providers can be temporarily rate-limited or unavailable.
    """
    last_error = None
    for attempt in range(1, max_retries + 1):
        try:
            return detect_allergens(extracted_text)
        except Exception as e:
            last_error = e
            if attempt < max_retries:
                time.sleep(delay_seconds)

    raise last_error