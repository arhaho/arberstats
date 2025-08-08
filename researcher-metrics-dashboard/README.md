# Researcher Metrics Dashboard (Free, No Scraping)

A lightweight web app that **tracks authors you select** and **auto-refreshes every 24h** using the free [OpenAlex API].
No scraping. No paid keys. Deploy anywhere that serves static files (GitHub Pages, Netlify, Vercel).

**What you get:**
- Total papers, total citations, h-index, i10-index per author
- Per-year papers and citations (last 10 years)
- Your selected authors are stored statically in `authors.yml`
- A GitHub Action (`.github/workflows/refresh.yml`) updates `frontend/data/snapshot.json` daily

> Why not Google Scholar? They do not provide a public API and scraping violates their Terms. OpenAlex is free, open, and stable.

## Quick Start

1) **Create a new GitHub repo** (private or public).  
2) **Download this ZIP**, extract, and push the contents to your repo.
3) Edit `scripts/authors.yml` to list the authors you want to track (OpenAlex IDs).  
   - Use `scripts/search_authors.py "First Last"` to discover IDs.
   - Or use `scripts/search_by_institution.py "University of Pristina"` to discover authors by institution.
4) In `scripts/refresh.py`, set your contact email in `OPENALEX_MAILTO` (recommended by OpenAlex).
5) Commit changes.  
6) **Enable GitHub Pages** or deploy `/frontend` folder to Netlify/Vercel (no build step needed).
7) The **daily refresh** GitHub Action runs at 03:00 UTC, updating `frontend/data/snapshot.json` with fresh stats.

### Local preview

You can open `frontend/index.html` directly in a browser. For local dev with a server:
```bash
python3 -m http.server --directory frontend 8000
# open http://localhost:8000
```

### Files of interest
- `scripts/authors.yml` — your static tracking list of authors (OpenAlex IDs)
- `scripts/refresh.py` — pulls data from OpenAlex and writes `frontend/data/snapshot.json`
- `scripts/search_authors.py` — find author IDs by name
- `scripts/search_by_institution.py` — find author IDs by institution name
- `.github/workflows/refresh.yml` — schedules and commits daily refresh

### Data Source
- OpenAlex API (free, no auth, 100k req/day). See docs: https://docs.openalex.org/

---

## FAQ

**Q: Can I add authors by clicking in the web UI?**  
For a 100% free/static stack, selection is kept in `scripts/authors.yml`. Edit it in GitHub’s UI (fast) and the next daily run will pick them up.

**Q: Can I force a manual refresh now?**  
Yes. In GitHub Actions, hit “Run workflow” on the *Daily Refresh* workflow.

**Q: Can I include h-index?**  
Yes — it’s included via `author.summary_stats.h_index` from OpenAlex.

**Q: Is this compliant?**  
Yes — it uses OpenAlex’s public API. No scraping of Google Scholar.

---

## License
MIT
