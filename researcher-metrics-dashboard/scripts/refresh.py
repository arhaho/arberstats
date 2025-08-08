#!/usr/bin/env python3
import os, json, time, requests, yaml, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_OUT = ROOT / "frontend" / "data" / "snapshot.json"

# Put your contact email here so OpenAlex can reach you if needed (recommended)
OPENALEX_MAILTO = os.getenv("OPENALEX_MAILTO", "arber.hoti@uni-pr.edu")

def get_author(author_id: str):
    url = f"https://api.openalex.org/authors/{author_id}"
    params = {"mailto": OPENALEX_MAILTO}
    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    return r.json()

def slim_author(a: dict):
    # Extract only what we need
    display_name = a.get("display_name")
    openalex_id = a.get("id")
    ids = a.get("ids", {})
    works_count = a.get("works_count")
    cited_by_count = a.get("cited_by_count")
    counts_by_year = a.get("counts_by_year", []) or []
    summary_stats = a.get("summary_stats", {}) or {}
    last_known_institutions = a.get("last_known_institutions", []) or []
    updated_date = a.get("updated_date")

    # flatten institutions
    inst_names = [i.get("display_name") for i in last_known_institutions if isinstance(i, dict)]

    return {
        "id": openalex_id,  # full URI like https://openalex.org/Axxxxx
        "openalex_key": openalex_id.split("/")[-1] if openalex_id else None,
        "display_name": display_name,
        "works_count": works_count,
        "cited_by_count": cited_by_count,
        "h_index": summary_stats.get("h_index"),
        "i10_index": summary_stats.get("i10_index"),
        "two_year_mean_citedness": summary_stats.get("2yr_mean_citedness"),
        "counts_by_year": counts_by_year,  # list of {year, works_count, cited_by_count}
        "institutions": inst_names,
        "updated_date": updated_date,
        "works_api_url": a.get("works_api_url"),
        "ids": ids,
    }

def main():
    cfg = yaml.safe_load(open(ROOT / "scripts" / "authors.yml", "r", encoding="utf-8"))
    author_ids = [row["id"] for row in cfg.get("authors", [])]

    out = {
        "generated_at_utc": datetime.datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "source": "OpenAlex",
        "authors": [],
    }

    for aid in author_ids:
        try:
            a = get_author(aid)
            out["authors"].append(slim_author(a))
            time.sleep(0.3)  # be gentle
        except Exception as e:
            out["authors"].append({
                "openalex_key": aid,
                "error": str(e),
            })

    DATA_OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"wrote {DATA_OUT}")

if __name__ == "__main__":
    main()
