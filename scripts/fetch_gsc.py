#!/usr/bin/env python3
"""
Google Search Console Data Fetcher
Fetches search performance data and saves to data/raw/gsc_dump.csv

Prerequisites:
1. Create a Google Cloud project
2. Enable Search Console API
3. Create OAuth 2.0 credentials (Desktop app)
4. Download credentials.json to scripts/ directory
5. Add your site to Search Console and verify ownership

Usage:
    python fetch_gsc.py --site https://windward.ai --days 30
"""

import argparse
import os
import json
from datetime import datetime, timedelta
from pathlib import Path

try:
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    import pandas as pd
except ImportError:
    print("Required packages not installed. Run: pip install -r requirements.txt")
    exit(1)

# Configuration
SCOPES = ['https://www.googleapis.com/auth/webmasters.readonly']
CREDENTIALS_FILE = Path(__file__).parent / 'credentials.json'
TOKEN_FILE = Path(__file__).parent / 'token.json'
OUTPUT_DIR = Path(__file__).parent.parent / 'data' / 'raw'

def authenticate():
    """Authenticate with Google Search Console API."""
    creds = None

    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CREDENTIALS_FILE.exists():
                print(f"Error: {CREDENTIALS_FILE} not found.")
                print("Download OAuth credentials from Google Cloud Console.")
                return None
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_FILE), SCOPES)
            creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())

    return creds

def fetch_search_data(service, site_url, start_date, end_date, row_limit=25000):
    """Fetch search analytics data from GSC."""
    request = {
        'startDate': start_date,
        'endDate': end_date,
        'dimensions': ['query', 'page', 'date'],
        'rowLimit': row_limit,
        'startRow': 0
    }

    all_rows = []
    while True:
        response = service.searchanalytics().query(siteUrl=site_url, body=request).execute()
        rows = response.get('rows', [])

        if not rows:
            break

        all_rows.extend(rows)

        if len(rows) < row_limit:
            break

        request['startRow'] += row_limit
        print(f"  Fetched {len(all_rows)} rows...")

    return all_rows

def process_data(rows):
    """Process GSC response into DataFrame."""
    data = []
    for row in rows:
        data.append({
            'query': row['keys'][0],
            'page': row['keys'][1],
            'date': row['keys'][2],
            'clicks': row.get('clicks', 0),
            'impressions': row.get('impressions', 0),
            'ctr': row.get('ctr', 0),
            'position': row.get('position', 0)
        })

    return pd.DataFrame(data)

def main():
    parser = argparse.ArgumentParser(description='Fetch Google Search Console data')
    parser.add_argument('--site', default='sc-domain:windward.ai', help='Site URL (use sc-domain: prefix for domain properties)')
    parser.add_argument('--days', type=int, default=30, help='Number of days to fetch')
    args = parser.parse_args()

    print(f"Fetching GSC data for {args.site}...")

    # Authenticate
    creds = authenticate()
    if not creds:
        return

    service = build('searchconsole', 'v1', credentials=creds)

    # Calculate date range
    end_date = (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d')  # GSC has 3-day delay
    start_date = (datetime.now() - timedelta(days=args.days + 3)).strftime('%Y-%m-%d')

    print(f"Date range: {start_date} to {end_date}")

    # Fetch data
    rows = fetch_search_data(service, args.site, start_date, end_date)

    if not rows:
        print("No data returned from GSC.")
        return

    # Process and save
    df = process_data(rows)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_file = OUTPUT_DIR / 'gsc_dump.csv'
    df.to_csv(output_file, index=False)

    print(f"\nSaved {len(df)} rows to {output_file}")
    print(f"Unique queries: {df['query'].nunique()}")
    print(f"Unique pages: {df['page'].nunique()}")
    print(f"Total clicks: {df['clicks'].sum()}")
    print(f"Total impressions: {df['impressions'].sum()}")

if __name__ == '__main__':
    main()
