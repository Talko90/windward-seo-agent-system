#!/usr/bin/env python3
"""
PageSpeed Insights Data Fetcher
Fetches Core Web Vitals and saves to data/raw/pagespeed_results.json

This uses the FREE PageSpeed Insights API (no auth required for basic usage).
For higher rate limits, get an API key from Google Cloud Console.

Usage:
    python fetch_pagespeed.py --url https://windward.ai
    python fetch_pagespeed.py --sitemap https://windward.ai/sitemap.xml --limit 20
"""

import argparse
import json
import os
import time
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Required packages not installed. Run: pip install requests beautifulsoup4")
    exit(1)

# Configuration
PSI_API_URL = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
OUTPUT_DIR = Path(__file__).parent.parent / 'data' / 'raw'
SCRIPTS_DIR = Path(__file__).parent

def load_api_key():
    """Load PageSpeed API key from scripts/.env or environment."""
    # Check environment variable first
    key = os.environ.get('PAGESPEED_API_KEY')
    if key:
        return key
    # Fall back to .env file in scripts directory
    env_file = SCRIPTS_DIR / '.env'
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                k, v = line.split('=', 1)
                if k.strip() == 'PAGESPEED_API_KEY':
                    return v.strip()
    return None

def fetch_pagespeed(url, strategy='mobile', api_key=None):
    """Fetch PageSpeed Insights for a URL."""
    params = {
        'url': url,
        'strategy': strategy,
        'category': ['performance', 'accessibility', 'best-practices', 'seo']
    }

    if api_key:
        params['key'] = api_key

    try:
        response = requests.get(PSI_API_URL, params=params, timeout=60)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"  Error fetching {url}: {e}")
        return None

def extract_metrics(psi_data):
    """Extract key metrics from PSI response."""
    if not psi_data:
        return None

    try:
        lighthouse = psi_data.get('lighthouseResult', {})
        categories = lighthouse.get('categories', {})
        audits = lighthouse.get('audits', {})

        # Core Web Vitals
        cwv = {
            'lcp': audits.get('largest-contentful-paint', {}).get('numericValue'),
            'fid': audits.get('max-potential-fid', {}).get('numericValue'),
            'cls': audits.get('cumulative-layout-shift', {}).get('numericValue'),
            'inp': audits.get('interaction-to-next-paint', {}).get('numericValue'),
            'ttfb': audits.get('server-response-time', {}).get('numericValue'),
            'fcp': audits.get('first-contentful-paint', {}).get('numericValue'),
        }

        # Category scores
        scores = {
            'performance': categories.get('performance', {}).get('score'),
            'accessibility': categories.get('accessibility', {}).get('score'),
            'best_practices': categories.get('best-practices', {}).get('score'),
            'seo': categories.get('seo', {}).get('score'),
        }

        return {
            'core_web_vitals': cwv,
            'scores': scores,
            'final_url': lighthouse.get('finalUrl'),
        }
    except Exception as e:
        print(f"  Error extracting metrics: {e}")
        return None

def fetch_sitemap_urls(sitemap_url, limit=None):
    """Fetch URLs from a sitemap or sitemap index."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    }
    try:
        response = requests.get(sitemap_url, headers=headers, timeout=30)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'lxml-xml')

        # Check if this is a sitemap index (contains <sitemap> tags)
        sub_sitemaps = soup.find_all('sitemap')
        if sub_sitemaps:
            print(f"  Sitemap index found with {len(sub_sitemaps)} sub-sitemaps")
            # Prioritize page and post sitemaps over landing pages, etc.
            priority_order = ['page-sitemap', 'post-sitemap']
            sub_urls = [s.find('loc').text for s in sub_sitemaps if s.find('loc')]

            ordered = []
            for prio in priority_order:
                ordered.extend([u for u in sub_urls if prio in u])
            ordered.extend([u for u in sub_urls if u not in ordered])

            all_page_urls = []
            for sub_url in ordered:
                if limit and len(all_page_urls) >= limit:
                    break
                print(f"  Fetching sub-sitemap: {sub_url}")
                sub_resp = requests.get(sub_url, headers=headers, timeout=30)
                if sub_resp.status_code == 200:
                    sub_soup = BeautifulSoup(sub_resp.content, 'lxml-xml')
                    page_urls = [loc.text for loc in sub_soup.find_all('loc')]
                    page_urls = [u for u in page_urls if not any(ext in u for ext in ['.jpg', '.png', '.pdf'])]
                    all_page_urls.extend(page_urls)
                else:
                    print(f"    Skipped (HTTP {sub_resp.status_code})")
                time.sleep(0.5)

            if limit:
                all_page_urls = all_page_urls[:limit]
            return all_page_urls

        # Regular sitemap — extract page URLs directly
        urls = [loc.text for loc in soup.find_all('loc')]
        urls = [u for u in urls if not any(ext in u for ext in ['.jpg', '.png', '.pdf'])]

        if limit:
            urls = urls[:limit]

        return urls
    except Exception as e:
        print(f"Error fetching sitemap: {e}")
        return []

def main():
    parser = argparse.ArgumentParser(description='Fetch PageSpeed Insights data')
    parser.add_argument('--url', help='Single URL to analyze')
    parser.add_argument('--sitemap', help='Sitemap URL to analyze multiple pages')
    parser.add_argument('--limit', type=int, default=10, help='Max pages to analyze from sitemap')
    parser.add_argument('--api-key', help='Google API key (optional, for higher rate limits)')
    parser.add_argument('--strategy', default='mobile', choices=['mobile', 'desktop'])
    args = parser.parse_args()

    # Auto-load API key from .env if not provided via command line
    if not args.api_key:
        args.api_key = load_api_key()
        if args.api_key:
            print(f"Using API key from scripts/.env")

    if not args.url and not args.sitemap:
        args.url = 'https://windward.ai'

    results = {
        'fetched_at': datetime.now().isoformat(),
        'strategy': args.strategy,
        'pages': []
    }

    # Get URLs to analyze
    if args.sitemap:
        print(f"Fetching URLs from sitemap: {args.sitemap}")
        urls = fetch_sitemap_urls(args.sitemap, args.limit)
        print(f"Found {len(urls)} URLs to analyze")
    else:
        urls = [args.url]

    # Analyze each URL
    for i, url in enumerate(urls):
        print(f"\n[{i+1}/{len(urls)}] Analyzing: {url}")

        psi_data = fetch_pagespeed(url, args.strategy, args.api_key)
        metrics = extract_metrics(psi_data)

        if metrics:
            page_result = {
                'url': url,
                **metrics
            }
            results['pages'].append(page_result)

            # Print summary
            scores = metrics.get('scores', {})
            cwv = metrics.get('core_web_vitals', {})
            print(f"  Performance: {scores.get('performance', 0)*100:.0f}%")
            print(f"  SEO: {scores.get('seo', 0)*100:.0f}%")
            print(f"  LCP: {cwv.get('lcp', 0)/1000:.2f}s")

        # Rate limiting (be nice to the API)
        if i < len(urls) - 1:
            time.sleep(2)

    # Save results
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_file = OUTPUT_DIR / 'pagespeed_results.json'

    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n\nSaved results to {output_file}")
    print(f"Analyzed {len(results['pages'])} pages")

    # Summary
    if results['pages']:
        avg_perf = sum(p['scores']['performance'] or 0 for p in results['pages']) / len(results['pages'])
        avg_seo = sum(p['scores']['seo'] or 0 for p in results['pages']) / len(results['pages'])
        print(f"\nAverage Performance Score: {avg_perf*100:.0f}%")
        print(f"Average SEO Score: {avg_seo*100:.0f}%")

if __name__ == '__main__':
    main()
