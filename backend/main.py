import os
import json
import httpx
from bs4 import BeautifulSoup
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
from google.genai import types

app = FastAPI(title="EcoCheck API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None

class AuditRequest(BaseModel):
    brand_name: str
    target_url: str | None = None

async def scrape_sustainability_text(url: str) -> str:
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as http_client:
            response = await http_client.get(url, headers=headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                for element in soup(["script", "style", "nav", "footer", "header"]):
                    element.extract()
                text = soup.get_text(separator=" ", strip=True)
                return text[:4000]
    except Exception as e:
        print(f"Scraping error: {e}")
    return ""

@app.post("/api/audit")
async def audit_brand(request: AuditRequest):
    if not client:
        raise HTTPException(
            status_code=500, 
            detail="GEMINI_API_KEY environment variable is not configured."
        )

    scraped_text = ""
    if request.target_url:
        scraped_text = await scrape_sustainability_text(request.target_url)

    prompt = f"""
    You are an expert ESG Auditor and Greenwashing Detection Engine.
    Analyze the following brand and scraped web context for sustainability claims vs greenwashing risks.

    Brand Name: {request.brand_name}
    Scraped Sustainability Web Context: {scraped_text if scraped_text else "No direct web text scraped. Rely on knowledge base for public ESG records of this brand."}

    Output MUST be strictly valid JSON matching this schema:
    {{
      "brand_name": "{request.brand_name}",
      "overall_score": <Integer from 0 to 100, where 100 is fully authentic and 0 is severe greenwashing>,
      "risk_level": "<LOW | MEDIUM | HIGH | SEVERE>",
      "summary": "<2-sentence executive summary of sustainability authenticity>",
      "claims": [
        {{
          "claim": "<Specific marketing claim>",
          "verdict": "<VERIFIED | VAGUE | MISLEADING | GREENWASHING>",
          "reality": "<Fact-check or real-world watchdog evidence>",
          "flag_level": "<RED | YELLOW | GREEN>"
        }}
      ],
      "metrics": {{
        "carbon_transparency": "<High | Medium | Low | None>",
        "supply_chain_audits": "<Verified | Partial | Unverified>",
        "vagueness_index": "<High | Moderate | Low>"
      }}
    }}
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.2,
            )
        )
        return json.loads(response.text)
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"AI Engine Audit Failed: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
