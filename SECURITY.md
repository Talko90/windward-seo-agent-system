# Security Guide for Contributors and Forkers

This repo is a public template. Before you fork and configure it for your own site, read this.

---

## What is Safe to Commit

| File | Safe? | Notes |
|------|-------|-------|
| `index.html` | ✅ Yes | Static dashboard — no credentials |
| `CLAUDE.md` | ✅ Yes | Architecture config — use placeholders |
| `skills.md` | ✅ Yes | Agent learnings database |
| `.claude/commands/*.md` | ✅ Yes | Agent slash commands |
| `scripts/*.py` | ✅ Yes | Scripts use env vars, not hardcoded keys |
| `scripts/.env.example` | ✅ Yes | Template only — no real values |
| `scripts/run-seo-pipeline.sh` | ✅ Yes | Shell script — no secrets |

---

## What Must NEVER Be Committed

| File | Why |
|------|-----|
| `scripts/.env` | Contains real API keys (GSC, GA4, Slack webhook) |
| `scripts/credentials.json` | Google OAuth client credentials |
| `scripts/token.json` | Google OAuth access/refresh tokens |
| `scripts/token_ga4.json` | GA4-specific OAuth tokens |
| `data/` directory | Contains raw analytics exports, pipeline reports, content drafts |
| Any `*.pem`, `*.key`, `*.p12` files | Private keys |

**All of the above are already in `.gitignore`.** This file exists so you understand *why* — not to replace the gitignore.

---

## Configuring Credentials

Never paste API keys directly into any `.md` or `.py` file. Always use environment variables:

```bash
# scripts/.env (gitignored)
GSC_SITE_URL=https://your-domain.com
GOOGLE_CREDENTIALS_PATH=scripts/credentials.json
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/REAL/WEBHOOK
AHREFS_API_KEY=your_ahrefs_key
```

Reference them in Python scripts as:
```python
import os
webhook = os.getenv('SLACK_WEBHOOK_URL')
```

---

## CLAUDE.md Placeholders

`CLAUDE.md` uses these placeholders — replace them before your first pipeline run:

| Placeholder | Replace With |
|-------------|-------------|
| `YOUR_GOOGLE_SHEETS_ID` | Your Google Sheets spreadsheet ID |
| `YOUR_SLACK_WEBHOOK_URL` | Your Slack incoming webhook URL |
| `YOUR_GOOGLE_DOC_ID_CONTENT_PRIORITIES` | Your content priorities doc ID |

---

## Public Content Rules

If you publish pipeline outputs publicly (dashboards, blog posts, demos):

- **Never include** specific customer company names
- **Never include** non-public vessel IMO numbers
- **Never include** internal metrics with exact counts — round up (`"50,000+"` not `"52,347"`)
- **Never include** absolute file paths (`/Users/yourname/...`)
- **Rotate** your Slack webhook URL if it was ever accidentally committed

---

## Reporting Security Issues

If you find a credential leak or security issue in this repo, please open a GitHub issue marked `[SECURITY]` or contact the maintainer directly before disclosing publicly.
