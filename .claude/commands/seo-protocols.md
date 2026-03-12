# Shared Agent Protocols

These protocols are referenced by all SEO agents. Follow them exactly when the relevant action is needed.

## Google Sheets Sync Protocol
1. Read current data → write updated data → verify `updatedCells > 0`
2. If fails: log to `data/reports/sheets_sync_errors.log`, continue workflow

## Google Drive Upload Protocol
1. Save locally → `python3 scripts/upload_to_drive.py "<file>" "<title>" "YOUR_GOOGLE_DRIVE_FOLDER_ID"`
2. Capture URL from stdout. If fails: retry once → log error → "Manual upload needed" in Slack
3. Update Sheet tab (Content Calendar, Glossary Backlog) with URL

## Content Existence Check Protocol
1. WebFetch target URL before proposing "create new page"
2. If exists → propose "optimize" not "create". Glossary URLs: `/glossary/what-is-[term]/`
3. Windward has 389+ glossary entries — always check first

## Dashboard Regeneration Protocol
**MANDATORY** after `/seo-plan` or `/seo-pipeline`:
1. Read all master data + raw data files
2. Regenerate `docs/seo-agents-dashboard.html` (update data, preserve HTML/CSS/JS)
3. Verify file > 20KB. Non-blocking if fails.

## Slack Notification Protocol
1. Build Block Kit JSON → send via curl to webhook → verify "ok" response
2. Webhook: `YOUR_SLACK_WEBHOOK_URL`
3. If fails: log to `data/reports/slack_errors.log`, continue workflow

## Reference Document Loading Protocol
1. Read `data/context/reference_docs.json` for doc IDs
2. Read `data/context/style_guide.md` for brand voice and formatting rules
3. Load Content Priorities via `python3 scripts/read_from_drive.py <doc_id>`
4. Check Content Feedback sheet for patterns. Match persona to active campaign.

## Style Guide Compliance Protocol
1. Read `data/context/style_guide.md` + appropriate persona file
2. Check: restricted military terms (BLOCKING), no banned opening constructions, American English, em dashes, vessel names italicized, no exclamation marks
3. Editorial posture: intelligence briefer, not marketer. Never fabricate vessel names/IMOs/dates.

## Low-Hanging Fruits Protocol (NEW — All Proposal Agents)

Every proposal agent MUST include a `low_hanging_fruits` array as the FIRST section in its output.

**Definition:** Impact Score > 60 AND Effort = 1

Each low-hanging fruit item must include:
```json
{
  "title": "Short description of the action",
  "target_url": "/page/path",
  "action": "Specific action to take",
  "impact_score": 72,
  "effort": 1,
  "why_this_matters": "One plain-English sentence explaining the business reason.",
  "data_source": "gsc_data | ahrefs_mcp | web_fetch",
  "confidence": 0.9
}
```

| Agent | Low-Hanging Fruit Examples |
|-------|--------------------------|
| `/seo-keywords` | Keywords at pos 5-15 with >500 impressions, fixable with title/meta changes |
| `/seo-competitors` | Gaps where we have a page but competitor outranks with better optimization |
| `/seo-geo` | Pages with AI Fitness < 50 fixable with simple formatting |
| `/seo-technical` | Missing alt text, meta length issues, simple schema additions |
| `/seo-links` | Unlinked brand mentions, broken link reclamation |

## Ahrefs Budget Reference (Per-Agent)

| Agent | Budget | Key Rules |
|---|---|---|
| `/seo-data` | ~1,500-2,000 units | Reduced limits (25 max), dropped duplicates |
| `/seo-keywords` | ~2,500-3,500 units | 3 clusters not 5, cache reuse, +750-1000 for SERP weakness analysis |
| `/seo-competitors` | ~1,800-2,500 units | Cache reuse, 3 competitors not 5 |
| `/seo-links` | ~400-600 units | Cache reuse, 3 competitors not 5 |

Budget guards (enforced by `/seo-data` Phase 0):
- Remaining < 20,000 → **ABORT** all Ahrefs calls, use cached data only
- Remaining < 50,000 → **MINIMAL mode**: domain metrics only
- Remaining > 50,000 → **FULL mode**: all calls within budgets
