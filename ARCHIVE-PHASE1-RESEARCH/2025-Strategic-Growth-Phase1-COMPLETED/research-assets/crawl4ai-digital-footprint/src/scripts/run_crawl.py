from digital_footprint.crawler import Crawler
import argparse
import csv
import os
import re
import time
from datetime import datetime
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from urllib import robotparser

USER_AGENT = "Crawl4AI/1.0 (+https://your-org.example)"


def allowed_to_fetch(base_url, user_agent, path="/"):
    rp = robotparser.RobotFileParser()
    robots_url = urljoin(base_url, "/robots.txt")
    try:
        rp.set_url(robots_url)
        rp.read()
        return rp.can_fetch(user_agent, path)
    except Exception:
        return True


def normalize_seed(seed):
    seed = seed.strip()
    if re.search(r"\.\w{2,}$", seed):  # looks like a domain
        if not seed.startswith("http"):
            seed = "https://" + seed
    else:
        # treat as brand / name: return None for fetch seeds
        seed = None
    return seed


def fetch_page(url, session, timeout=10):
    try:
        r = session.get(url, timeout=timeout)
        r.raise_for_status()
        return r.text
    except Exception:
        return None


def extract_meta(html):
    soup = BeautifulSoup(html, "html.parser")
    title = soup.title.string.strip() if soup.title and soup.title.string else ""
    desc = ""
    d = soup.find("meta", attrs={"name": "description"})
    if d and d.get("content"):
        desc = d["content"].strip()
    text = " ".join([p.get_text(" ", strip=True) for p in soup.find_all("p")])[:800]
    return title, desc, text


def crawl_domain(seed_url, max_pages=50, delay=1.0):
    parsed = urlparse(seed_url)
    base = f"{parsed.scheme}://{parsed.netloc}"
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})
    to_visit = {seed_url}
    visited = set()
    results = []

    while to_visit and len(visited) < max_pages:
        url = to_visit.pop()
        if url in visited:
            continue
        path = urlparse(url).path or "/"
        if not allowed_to_fetch(base, USER_AGENT, path):
            visited.add(url)
            continue
        html = fetch_page(url, session)
        visited.add(url)
        if not html:
            continue
        title, desc, snippet = extract_meta(html)
        results.append({"url": url, "domain": parsed.netloc, "title": title, "description": desc, "snippet": snippet})
        soup = BeautifulSoup(html, "html.parser")
        for a in soup.find_all("a", href=True):
            href = a["href"].strip()
            if href.startswith("#") or href.startswith("mailto:") or href.startswith("tel:"):
                continue
            joined = urljoin(base, href)
            jp = urlparse(joined)
            if jp.netloc == parsed.netloc:
                if joined not in visited:
                    to_visit.add(joined)
        time.sleep(delay)
    return results


def save_csv(rows, out_path):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["collected_at", "seed", "url", "domain", "title", "description", "snippet"])
        writer.writeheader()
        for r in rows:
            writer.writerow(r)


def main():
    parser = argparse.ArgumentParser(description="Simple Crawl4AI footprint scanner")
    parser.add_argument("--targets", required=True, help="Comma separated seeds (domains or brand names)")
    parser.add_argument("--out", default="outputs/footprint.csv", help="Output CSV path")
    parser.add_argument("--max-pages", type=int, default=50, help="Max pages per domain")
    parser.add_argument("--delay", type=float, default=1.0, help="Delay between requests (seconds)")
    args = parser.parse_args()

    seeds = [s.strip() for s in args.targets.split(",") if s.strip()]
    all_rows = []
    ts = datetime.utcnow().isoformat()

    for seed in seeds:
        fetch_seed = normalize_seed(seed)
        if fetch_seed:
            print(f"[crawl] scanning domain seed: {fetch_seed}")
            results = crawl_domain(fetch_seed, max_pages=args.max_pages, delay=args.delay)
            for r in results:
                all_rows.append({
                    "collected_at": ts,
                    "seed": seed,
                    "url": r["url"],
                    "domain": r["domain"],
                    "title": r["title"],
                    "description": r["description"],
                    "snippet": r["snippet"],
                })
        else:
            # brand/keyword seed: record for manual follow-up / external search (placeholder)
            print(f"[note] brand seed provided (no direct crawl): {seed}")
            all_rows.append({
                "collected_at": ts,
                "seed": seed,
                "url": "",
                "domain": "",
                "title": "BRAND_SEED",
                "description": "Brand / keyword seed — run external search (Google/Bing/APIs) and add results",
                "snippet": "",
            })

    print(f"[save] writing {len(all_rows)} rows to {args.out}")
    save_csv(all_rows, args.out)
    print("[done]")


if __name__ == "__main__":
    main()