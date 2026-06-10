from __future__ import annotations

import json
import logging
import re
import time
import requests
from dataclasses import dataclass
from pathlib import Path

from core.config import Settings
from core.utils import write_json, read_json

logger = logging.getLogger(__name__)

@dataclass(frozen=True)
class PaperRecord:
    paper_id: str
    title: str
    summary: str
    authors: list[str]
    categories: list[str]
    primary_category: str
    published: str
    updated: str
    abs_url: str
    pdf_url: str
    comment: str

def parse_crossref_payload(payload: dict) -> list[PaperRecord]:
    records = []
    items = payload.get("message", {}).get("items", [])
    
    for item in items:
        doi = item.get("DOI", "")
        if not doi:
            continue
            
        title_list = item.get("title", [])
        title = title_list[0] if title_list else "Unknown Title"
        
        abstract = item.get("abstract", "")
        abstract = re.sub(r'<[^>]+>', '', abstract) if abstract else ""
        
        authors = []
        for author in item.get("author", []):
            given = author.get("given", "")
            family = author.get("family", "")
            if given or family:
                authors.append(f"{given} {family}".strip())
                
        categories = item.get("subject", [])
        primary_category = categories[0] if categories else "Unknown"
        
        issued = item.get("issued", {}).get("date-parts", [[None]])[0]
        if issued and issued[0] is not None:
            year = issued[0]
            month = issued[1] if len(issued) > 1 else 1
            day = issued[2] if len(issued) > 2 else 1
            published = f"{year}-{month:02d}-{day:02d}T00:00:00Z"
        else:
            published = "2000-01-01T00:00:00Z"
            
        updated = published
        abs_url = item.get("URL", f"https://doi.org/{doi}")
        pdf_url = ""
        
        record = PaperRecord(
            paper_id=doi,
            title=title,
            summary=abstract,
            authors=authors,
            categories=categories,
            primary_category=primary_category,
            published=published,
            updated=updated,
            abs_url=abs_url,
            pdf_url=pdf_url,
            comment=""
        )
        records.append(record)
        
    return records

def fetch_source_records(settings: Settings) -> list[PaperRecord]:
    base_url = "https://api.crossref.org/works"
    params = {
        "query": settings.source_query,
        "filter": settings.source_filter,
        "rows": settings.max_results,
        "select": "DOI,title,author,abstract,subject,issued,URL,link"
    }
    
    headers = {"User-Agent": "AI-Lab10-Pipeline/1.0 (mailto:bot@example.com)"}
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.get(base_url, headers=headers, params=params, timeout=15)
            if response.status_code == 200:
                payload = response.json()
                write_json(settings.paths.raw_api_response, payload)
                records = parse_crossref_payload(payload)
                write_json(settings.paths.raw_records_json, [r.__dict__ for r in records])
                return records
            elif response.status_code in [429, 503]:
                time.sleep(2 ** attempt)
            else:
                response.raise_for_status()
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                raise RuntimeError(f"Failed to fetch Crossref data: {e}")
            time.sleep(2 ** attempt)
            
    raise RuntimeError("Failed to fetch Crossref data after max retries")

def load_raw_records(path: Path) -> list[PaperRecord]:
    records_dict = read_json(path)
    return [PaperRecord(**d) for d in records_dict]
