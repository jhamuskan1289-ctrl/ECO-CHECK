#  EcoCheck — AI-Powered Corporate Greenwashing Auditor

> **Kritikal Hacks Entry**  
> *Instantly audit corporate sustainability claims, detect greenwashing buzzwords, and cross-reference PR statements against real-world environmental watchdog data.*

---

##  Overview

Modern consumers want to support genuinely sustainable brands, but corporations frequently engage in **greenwashing**—using vague, unverified marketing buzzwords like *"eco-friendly"* or *"sustainably sourced"* while hiding rising carbon footprints inside dense, multi-page ESG reports.

**EcoCheck** is a full-stack, AI-driven auditor that automates the verification process:
1. **Crawls** corporate sustainability web portals, disclosures, and ESG reports.
2. **Searches** independent environmental news registries, regulatory penalty databases, and watchdog reports.
3. **Analyzes** marketing statements using Google Gemini API to calculate an **Authenticity Score (0–100)** and generate a **Claim vs. Reality** breakdown.

---

## Key Features

- **Automated Web Data Ingestion:** Scrapes unstructured DOM text, disclosures, and ESG web pages without requiring hardcoded APIs.
- **Vagueness & Buzzword Detection:** Flags claims lacking hard percentages, third-party certifications, or measurable metrics.
- **Cross-Source Contradiction Matrix:** Cross-references marketing PR against external watchdog penalties and news reports.
- **Real-Time Interactive Dashboard:** Renders an Authenticity Score Gauge, high-risk flag indicators, and a structured audit report.
- **Deterministic JSON API:** Standardized JSON pipeline powered by Gemini 2.5 Flash for reliable, repeatable evaluations.

---

##  Tech Stack

| Component | Technology Used | Purpose |
| :--- | :--- | :--- |
| **Frontend** | HTML5, Tailwind CSS, JavaScript (ES6+) | Sleek UI, score gauges, risk badges, and claim cards |
| **Backend API** | Python 3.11, FastAPI, Uvicorn | Lightweight asynchronous server coordinating API endpoints |
| **Data Scraping** | BeautifulSoup4, HTTPX, AsyncIO | Asynchronous web scraping & un-APId text extraction |
| **AI Engine** | Google Gemini API (`gemini-2.5-flash`) | NLP reasoning, greenwashing detection, and JSON parsing |

---

##  Getting Started

### Prerequisites
- Python 3.10+
- Google Gemini API Key

### Setup & Run
```bash
cd backend
pip install -r requirements.txt
export GEMINI_API_KEY="your_api_key_here"
python main.py
