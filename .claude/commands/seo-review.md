# /seo-review - Quality Assurance & Security Review Agent

**Purpose**: Validates proposals and content drafts for quality, accuracy, brand consistency, and security compliance before publication.

**When to Run**:
- Automatically in `/seo-pipeline` (after Phase 6, before Phase 8)
- Manually before publishing any content
- After major content updates

**Output**: Review report with pass/warning/fail status and actionable recommendations.

---

## What This Agent Does

Acts as the **quality gate** between proposal generation and content publication. Performs three types of review:

1. **Quality Review** → Validates accuracy, brand voice, SEO compliance
2. **Security Review** → Scans for data leaks, credential exposure, malicious links
3. **Context Review** → Ensures maritime domain accuracy and regulatory correctness

**Key Benefit**: Catches errors, security issues, and false positives BEFORE they reach content teams or live site.

---

## Review Checklist

### 1. Quality Review

#### A. Factual Accuracy
- [ ] **Maritime Terminology**: Vessel types, shipping terms used correctly (e.g., "bulk carrier" not "cargo bulk", "AIS" not "AIS system")
- [ ] **Regulatory Citations**: IMO regulations, OFAC sanctions lists correctly referenced with official document numbers
- [ ] **Competitor Data Freshness**: Publication dates < 30 days for "new content" claims (reject if older)
- [ ] **Metric Validation**: Traffic numbers, ranking positions match GSC data (cross-check against `data/raw/gsc_dump.csv`)
- [ ] **No Hallucinations**: All claims have supporting evidence (data source, web citation, or GSC record)
- [ ] **Data Citation Tags**: Every quantitative claim has `data_source`, `tool_used`, and `fetched_at` per Rule 4

#### A2. Anti-Hallucination Verification (MANDATORY — Rule 5 Enforcement)

**This check is REQUIRED on every QA run. Zero tolerance for unsourced numbers.**

**Step 1: Random Spot-Check (3 Claims)**
- Pick 3 random quantitative claims from the proposal (numbers, percentages, metrics)
- For each claim, verify against raw data files:
  - Ahrefs metrics → Check `data/raw/ahrefs_*.json` files
  - GSC metrics → Check `data/raw/gsc_dump.csv`
  - GA4 metrics → Check `data/raw/ga4_dump.csv` or `ga4_organic.csv`
  - Competitor data → Check `data/raw/ahrefs_competitors_snapshot.json`

**Step 2: Verify Data Source Tags**
- Every claim MUST have a `data_source` tag (ahrefs_mcp, gsc_data, ga4_data, web_search, calculated)
- Claims tagged `web_search` must have confidence ≤ 0.60
- Claims tagged `calculated` must show formula and input sources
- Claims with NO `data_source` tag → **WARNING**

**Step 3: Cross-Reference Check**
```bash
# For each sampled claim:
# 1. Extract the claimed value
# 2. Find the raw data file
# 3. Verify the number matches (within 5% tolerance for rounding)

# Example: Claim "windward.ai DR 64 (from Ahrefs)"
cat data/raw/ahrefs_domain_metrics.json | python3 -c "
import json, sys
data = json.load(sys.stdin)
print(f'DR from raw data: {data.get(\"domain_rating\", \"NOT FOUND\")}')
"
```

**Scoring:**
- **VERIFIED** (3/3 claims check out): Proposal approved
- **PARTIALLY_VERIFIED** (1-2/3 claims fail): **WARNING** — flag failed claims, allow processing with notes
- **UNVERIFIED** (0/3 claims check out): **BLOCKING** — return proposal to originating agent for data citation fixes

**Log results:**
```bash
echo "[$(date)] ANTI-HALLUCINATION CHECK: [proposal_name] — [VERIFIED/PARTIALLY/UNVERIFIED] — [details]" >> data/reports/hallucination_checks.log
```

**Validation Method**:
```bash
# Check competitor content dates
if claim includes "new competitor content":
    publication_date = extract_date_from_proposal
    days_old = today - publication_date
    if days_old > 7:
        flag_as_warning("Competitor content not new (>7 days)")

# Validate keyword opportunities against GSC + Ahrefs
if claim includes "keyword opportunity":
    grep -i "keyword_phrase" data/raw/gsc_dump.csv
    python3 -c "import json; data=json.load(open('data/raw/ahrefs_keywords.json')); print([k for k in data if 'keyword_phrase' in str(k)])"
    if not found in either:
        flag_as_warning("Keyword not in GSC or Ahrefs data (may be speculative)")
```

#### B. Brand Voice & Style Guide Compliance

Load `data/context/style_guide.md` before reviewing.

**Editorial Posture:**
- [ ] Content reads as senior intelligence briefer, NOT marketer/salesperson
- [ ] Reflects at least 3 of 7 brand traits (Mission-critical, Tech-first, Big picture, Sharp, Expert, Empowering, Trustworthy)
- [ ] No sensational language ("revolutionary", "game-changing", "best-in-class", "unprecedented")
- [ ] No hedging filler ("it's worth noting", "it should be said", "arguably", "it appears that")

**Brand & Terminology:**
- [ ] "Windward" capitalized consistently
- [ ] "Maritime AI" used correctly (not "AI Maritime")
- [ ] Terminology consistent throughout (pick one: don't alternate between "sanctions screening" and "compliance checks")
- [ ] CTA matches persona (commercial: "Request a Demo", government: "Request a Briefing")
- [ ] Uses approved positioning phrases for the target segment (see style_guide.md)
- [ ] Competitive positioning achieved through framing, NOT by naming competitors

**Formatting (BLOCKING if major violations):**
- [ ] American English (behavior not behaviour, analyze not analyse, defense not defence)
- [ ] Em dashes (—) not en dashes or hyphens for clause breaks
- [ ] Vessel names italicized
- [ ] No exclamation marks anywhere
- [ ] Periods after all bullet point items
- [ ] Subheads present — scannable structure

**Opening Sentence (WARNING):**
- [ ] No banned constructions: "The maritime industry is changing...", "In today's complex environment...", "As geopolitical tensions rise...", "Now more than ever...", "It's no secret that..."
- [ ] Leads with concrete data point, development, or operational reality

**Restricted Military Terminology (BLOCKING when attributed to Windward):**
- [ ] No "interception" (use: positional data, detection)
- [ ] No "surveillance" (use: monitoring)
- [ ] No "ISR tasking" (use: tipping/tasking)
- [ ] No "automated target generation" (use: automated risk generation)
- [ ] No "pattern-of-life baselines" (use: activity baselines/route patterns)
- [ ] No "proactive threat hunting" (use: proactive risk monitoring)
- [ ] No "evidence-grade" (remove entirely)
- [ ] Metrics qualified with "up to" (not "MTTD reduced by 80%" → "up to 80%")
Note: These terms ARE allowed when describing government/navy/enforcement actions. They are ONLY restricted when describing what Windward does.

**AI-Generated Content Rules:**
- [ ] Every data point, statistic, vessel name, IMO number has a cited/verifiable source
- [ ] No fabricated vessel names, company names, or enforcement actions
- [ ] Assessed conclusions marked with "Windward assesses..." or "Available data suggests..." — not presented as confirmed fact
- [ ] No invented dates or timelines (use [VERIFICATION NEEDED] if unsure)
- [ ] No fabricated Windward platform detection claims

**Validation Method**:
```bash
# Check for brand term inconsistencies
grep -i "windward" proposal.json | grep -v "Windward"  # lowercase usage
grep -E "(Shadow Fleet|Phantom Fleet)" proposal.json  # term variations

# Scan for restricted military terms attributed to Windward
for term in "interception" "surveillance" "ISR tasking" "automated target generation" "evidence-grade" "proactive threat hunting"; do
    matches=$(grep -in "$term" "$DRAFT_FILE" 2>/dev/null)
    if [ -n "$matches" ]; then
        if echo "$matches" | grep -iq "windward\|our platform\|we provide\|our solution"; then
            echo "BLOCKING: Restricted term '$term' attributed to Windward"
        else
            echo "WARNING: Restricted term '$term' found — verify not attributed to Windward"
        fi
    fi
done

# Check for banned openers
head -5 "$DRAFT_FILE" | grep -iE "(maritime industry is changing|in today.s complex|geopolitical tensions rise|now more than ever|it.s no secret)"

# Check for exclamation marks
grep -n "!" "$DRAFT_FILE"
```

#### C. Technical SEO Compliance
- [ ] **Schema Validation**: Recommended schema types valid per Schema.org specs (use schema.org/docs/schemas.html)
- [ ] **Meta Description Length**: 50-160 characters (flag if outside range)
- [ ] **Title Tag Length**: 50-60 characters (flag if outside range)
- [ ] **Heading Hierarchy**: H1 → H2 → H3 (no skips like H1 → H3)
- [ ] **Internal Link Validity**: All windward.ai URLs return 200 status (check via HEAD request or sitemap)

**Validation Method**:
```bash
# Validate schema type
schema_type = extract_schema_type_from_proposal
curl -s "https://schema.org/$schema_type" | grep -q "rdfs:Class"
if [ $? -ne 0 ]; then
    flag_as_blocking("Invalid schema type: $schema_type")
fi

# Check meta description length
meta_length = len(meta_description)
if meta_length < 50 or meta_length > 160:
    flag_as_warning("Meta description length suboptimal: $meta_length chars")
```

---

### 2. Security Review

#### A. Sensitive Data Exposure (BLOCKING)
- [ ] **Customer Names**: Scan for known Windward customer company names (maintain list in `data/context/customer_names.txt`)
- [ ] **Non-Public IMO Numbers**: Validate IMO numbers against public registries (IMO Public Register, OFAC SDN list)
- [ ] **Credential Leaks**: Scan for API keys, tokens, passwords (patterns: `API_KEY`, `Bearer`, `sk-`, etc.)
- [ ] **Internal Emails**: Check for @windward.ai email addresses in public-facing content
- [ ] **File Paths**: No absolute paths exposed (e.g., `~/...`)

**Validation Method**:
```bash
# Scan for customer names (example - customize with actual customer list)
customer_names=("Vitol" "Trafigura" "Gunvor" "Glencore")  # EXAMPLE ONLY
for name in "${customer_names[@]}"; do
    if grep -qi "$name" proposal.json; then
        flag_as_blocking("Customer name detected: $name")
    fi
done

# Scan for IMO numbers (pattern: IMO followed by 7 digits)
imo_numbers=$(grep -oE "IMO[0-9]{7}" proposal.json)
for imo in $imo_numbers; do
    # Check if IMO is in public OFAC list or news articles
    public_check=$(curl -s "https://sanctionssearch.ofac.treas.gov/" | grep -q "$imo")
    if [ $? -ne 0 ]; then
        flag_as_blocking("Non-public IMO number detected: $imo")
    fi
done

# Scan for API keys
if grep -qE "(api[_-]?key|bearer|sk-|ghp_|gho_)" proposal.json; then
    flag_as_blocking("Potential credential leak detected")
fi

# Scan for absolute file paths
if grep -qE "/Users/[a-zA-Z]+|/home/[a-zA-Z]+|C:\\\\Users" proposal.json; then
    flag_as_warning("Absolute file path detected (sanitize before publish)")
fi
```

#### B. External Link Security
- [ ] **Phishing/Malware Check**: Validate external URLs against threat databases (VirusTotal, Google Safe Browsing)
- [ ] **HTTPS Enforcement**: All external links use HTTPS (not HTTP)
- [ ] **Link Rot**: Check if URLs return 200 status (flag 404s)

**Validation Method**:
```bash
# Extract external URLs from proposals
urls=$(grep -oE "https?://[a-zA-Z0-9./?=_-]+" proposal.json | grep -v "windward.ai")

for url in $urls; do
    # Check HTTP vs HTTPS
    if [[ $url == http://* ]]; then
        flag_as_warning("Non-HTTPS link: $url")
    fi

    # Check if URL is reachable
    status_code=$(curl -s -o /dev/null -w "%{http_code}" -L "$url")
    if [ "$status_code" == "404" ]; then
        flag_as_warning("Broken link (404): $url")
    fi
done
```

#### C. Schema Markup Security
- [ ] **Injection Vulnerabilities**: Validate JSON-LD schema doesn't contain executable code or script tags
- [ ] **XSS Prevention**: Check for `<script>`, `javascript:`, `onerror=` in schema content

**Validation Method**:
```bash
# Scan schema markup for injection patterns
if grep -qE "(<script|javascript:|onerror=|onclick=)" proposal.json; then
    flag_as_blocking("Potential XSS/injection in schema markup")
fi
```

#### D. MANDATORY: Legal Pre-Publishing Checklist

**This checklist is a HARD STOP — content that fails legal review MUST NOT be published until cleared.**

##### Vessel Sanctioning Check Flow
For ANY content mentioning specific vessels:

1. **Does content mention a specific vessel?**
   - NO → Proceed to General Legal Checks below
   - YES → Continue to Step 2

2. **Is the vessel sanctioned?**
   - **YES (Sanctioned):**
     - Check: Is ownership information updated?
     - Check: Is P&I (Protection & Indemnity) updated?
     - If either is NOT updated → **LEGAL_BLOCKED** — Flag for Casif/Joe C review
     - If both updated → Proceed with caution, mark **LEGAL_REVIEW_NEEDED**
   - **NOT Sanctioned:**
     - Only publish if: (a) zombie vessel, OR (b) previously covered in media for the same reason
     - If neither applies → **LEGAL_BLOCKED** — Do not publish vessel details

3. **Customer/Prospect Connection Check:**
   - Check all 7 levels of ownership for customer/prospect connections
   - If vessel's flag registry matches a customer's flag → Extra sensitivity, mark **LEGAL_REVIEW_NEEDED**
   - If Western-flag vessel → Extra sensitivity, mark **LEGAL_REVIEW_NEEDED**

4. **When in doubt:** Check with CS team or on SF (Salesforce)

##### Legal Review Status Tags
Every draft MUST include one of these tags in its metadata:

| Tag | Meaning | Action |
|-----|---------|--------|
| `LEGAL_CLEAR` | No items requiring legal review | Safe to publish after content review |
| `LEGAL_REVIEW_NEEDED` | Specific items flagged | List flagged items, send to legal team |
| `LEGAL_BLOCKED` | Must not publish without legal approval | **HARD STOP** — Do not proceed |

##### General Legal Checks (All Content)
- [ ] No customer company names mentioned (use generic descriptions)
- [ ] No non-public IMO numbers (unless from published sanctions list with citation)
- [ ] No internal Windward metrics exposed (use "50,000+" not "52,347")
- [ ] No credentials, API keys, or internal URLs in output
- [ ] External links validated (not phishing/malware, from reputable sources)
- [ ] File paths sanitized (no `/Users/...` paths)
- [ ] Statistics cited with sources and last-verified dates
- [ ] Approved data points match Content Priorities document

**Validation Method**:
```bash
# Check for specific vessel mentions (IMO numbers indicate specific vessels)
vessel_mentions=$(grep -oE "IMO[0-9]{7}" proposal.json)
if [ -n "$vessel_mentions" ]; then
    echo "⚠ Vessel-specific content detected — triggering legal check flow"
    for imo in $vessel_mentions; do
        # Check OFAC SDN for sanctioned status
        echo "CHECK: Is $imo sanctioned? Verify ownership + P&I are current"
        echo "CHECK: Run 7-level ownership check for customer/prospect connections"
    done
    echo "REQUIRED: Assign LEGAL_CLEAR, LEGAL_REVIEW_NEEDED, or LEGAL_BLOCKED tag"
fi

# Check draft metadata for legal tag
if ! grep -qE "LEGAL_(CLEAR|REVIEW_NEEDED|BLOCKED)" draft.md; then
    flag_as_blocking("Draft missing mandatory legal review tag")
fi
```

---

### 3. Context Review (Maritime Domain)

#### A. Maritime Domain Accuracy
- [ ] **Vessel Types**: Correct usage (VLCC, Aframax, Suezmax, Handysize, etc.)
- [ ] **Shipping Terms**: Proper terminology (ballast, laden, deadweight tonnage, draft)
- [ ] **Geographic Accuracy**: Correct strait names (Strait of Hormuz not "Hormuz Strait")
- [ ] **Industry Bodies**: Correct names (IMO = International Maritime Organization, not "International Marine Org")

**Validation Method**: Cross-reference against maritime glossary (`data/context/maritime_glossary.json` if exists, or Lloyd's List terminology guide)

#### B. Regulatory Compliance
- [ ] **OFAC Citations**: Correct formatting (e.g., "OFAC SDN List" not "OFAC Sanctions List")
- [ ] **IMO Regulations**: Cite by number (e.g., "IMO 2020 Sulphur Cap" or "MARPOL Annex VI")
- [ ] **Export Controls**: If mentioning dual-use technology, ensure compliance language present

**Validation Method**: Validate regulation numbers against official IMO/OFAC documents (web search or local reference)

---

## Review Severity Levels

### BLOCKING (Pipeline STOPS)
**Criteria**: Security issue or major factual error that must be fixed before publication

**Examples**:
- Customer name exposed
- Non-public IMO number in content
- Credential leak detected
- Phishing/malware link found
- Schema injection vulnerability

**Action**: Stop pipeline, do NOT generate content, report to user immediately

---

### WARNING (Pipeline CONTINUES)
**Criteria**: Quality issue or minor error that should be reviewed but doesn't block publication

**Examples**:
- Stale competitor data (> 30 days old)
- Unverified regulatory citation
- Brand term inconsistency
- Meta description length suboptimal
- Broken internal link (404)
- Non-HTTPS external link
- Maritime terminology minor error

**Action**: Flag in report, continue to content generation, user reviews before publishing

---

### PASS (No Issues)
**Criteria**: All checks passed, content safe and accurate

**Action**: Proceed to content generation without warnings

---

## Output Format

Review report saved to `data/reports/qa_review_[timestamp].json`:

```json
{
  "review_date": "2026-02-15T10:30:00Z",
  "pipeline_run_id": "pipeline-2026-02-15-1030",
  "overall_status": "WARNING",
  "blocking_issues": [],
  "warnings": [
    {
      "issue_id": "WARN-001",
      "category": "Quality - Data Freshness",
      "severity": "warning",
      "description": "Competitor analysis references Kpler content from 2026-01-10 (36 days old)",
      "location": "data/proposals/competitors_proposal.json line 45",
      "recommendation": "Re-run competitor analysis with fresh web search or remove stale reference",
      "auto_fixable": false
    },
    {
      "issue_id": "WARN-002",
      "category": "Technical SEO",
      "severity": "warning",
      "description": "Proposed meta description for ACT-047 is 165 characters (optimal: 50-160)",
      "location": "data/master/action_queue.json ACT-047",
      "recommendation": "Shorten meta description by 5 characters",
      "auto_fixable": false
    }
  ],
  "passed_checks": [
    "No customer names detected",
    "No credential leaks",
    "All external links HTTPS",
    "Schema markup valid",
    "Brand terms consistent",
    "Maritime terminology accurate"
  ],
  "recommendations": [
    "Review competitor content dates before finalizing blog draft",
    "Trim meta descriptions to optimal length"
  ],
  "statistics": {
    "total_checks": 28,
    "passed": 26,
    "warnings": 2,
    "blocking": 0,
    "scanned_files": [
      "data/proposals/keywords_proposal.json",
      "data/proposals/competitors_proposal.json",
      "data/proposals/geo_proposal.json",
      "data/proposals/technical_proposal.json",
      "data/master/action_queue.json"
    ]
  }
}
```

Human-readable summary saved to `data/reports/qa_review_[timestamp]_summary.txt`:

```
QA Review Summary - 2026-02-15 10:30 AM
========================================

STATUS: ⚠️ WARNING (2 issues, 0 blocking)

BLOCKING ISSUES: None ✅

WARNINGS (2):
1. [Quality] Competitor content stale (36 days old)
   → Recommendation: Re-run analysis or remove reference

2. [Technical SEO] Meta description too long (165 chars)
   → Recommendation: Trim by 5 characters

PASSED CHECKS (26):
✅ No customer names exposed
✅ No credential leaks
✅ All external links secure (HTTPS)
✅ Schema markup valid
✅ Brand terms consistent
✅ Maritime terminology accurate
... (20 more)

RECOMMENDATION:
Pipeline may proceed to content generation. Review warnings before publishing.

---
Files Scanned: 5 proposals, 1 master database
Total Checks: 28
Runtime: 45 seconds
```

---

## Workflow Integration

### In `/seo-pipeline` (Automated)

```bash
# Phase 6: Orchestration completes
/seo-plan  # Merges proposals, writes action_queue.json

# Phase 7: QA Review (AUTOMATIC)
/seo-review  # Scans proposals and action queue

# Decision Point:
if [ "$review_status" == "BLOCKING" ]; then
    echo "❌ BLOCKING ISSUES FOUND - Pipeline stopped"
    echo "Review report: data/reports/qa_review_*.json"
    exit 1
elif [ "$review_status" == "WARNING" ]; then
    echo "⚠️ WARNINGS FOUND - Proceeding with caution"
    echo "Review warnings before publishing drafts"
    # Continue to Phase 8
elif [ "$review_status" == "PASS" ]; then
    echo "✅ QA PASSED - Proceeding to content generation"
    # Continue to Phase 8
fi

# Phase 8: Content Generation (only if not blocked)
/seo-content
```

### Manual Standalone Use

```bash
# Before publishing any content
/seo-review

# Check output
cat data/reports/qa_review_*_summary.txt

# If BLOCKING → fix issues, re-run review
# If WARNING → review issues, decide to proceed or fix
# If PASS → safe to publish
```

---

## Customization

### Adding New Security Checks

Edit this file, add to checklist:

```markdown
#### D. New Security Check Category
- [ ] Check description
- [ ] Another check

**Validation Method**:
```bash
# Your custom validation script
```
```

### Maintaining Customer Name List

Update `data/context/customer_names.txt` (one per line):
```
Vitol
Trafigura
[Add known customers here]
```

**IMPORTANT**: This file is `.gitignore`'d for security. Do NOT commit to version control.

---

## Error Handling

**If QA review itself fails**:
- Log error to `data/reports/qa_review_errors.log`
- Send Slack notification with error details
- In `/seo-pipeline`, continue to Phase 8 (better to generate content with manual review than block entirely)
- Flag in final pipeline report: "⚠️ QA review failed - manual review required"

---

## Testing

### Positive Test Cases (Should Pass)
```json
{
  "test_case": "Valid maritime content",
  "content": "Windward's Maritime AI platform detects AIS spoofing by analyzing vessel movement patterns...",
  "expected": "PASS"
}
```

### Negative Test Cases (Should Fail/Warn)

**BLOCKING Test**:
```json
{
  "test_case": "Customer name exposure",
  "content": "Vitol uses Windward for sanctions screening",
  "expected": "BLOCKING - Customer name detected"
}
```

**WARNING Test**:
```json
{
  "test_case": "Stale competitor data",
  "content": "Kpler published new content on 2026-01-01",
  "today": "2026-02-15",
  "expected": "WARNING - Competitor content >30 days old"
}
```

Test suite location: `data/test/qa_test_cases.json` (to be created)

---

## Slack Notification

After review completes, send notification:

```bash
curl -X POST -H 'Content-type: application/json' \
  --data '{
    "blocks": [
      {
        "type": "header",
        "text": {"type": "plain_text", "text": "🛡️ SEO QA Review Complete", "emoji": true}
      },
      {
        "type": "section",
        "text": {"type": "mrkdwn", "text": "*Status:* ⚠️ WARNING (2 issues)\n*Blocking:* 0\n*Warnings:* 2"}
      },
      {
        "type": "section",
        "fields": [
          {"type": "mrkdwn", "text": "*Checks Run:*\n28"},
          {"type": "mrkdwn", "text": "*Passed:*\n26"}
        ]
      },
      {
        "type": "context",
        "elements": [{"type": "mrkdwn", "text": "Full report: `data/reports/qa_review_2026-02-15-1030_summary.txt`"}]
      }
    ]
  }' \
  'YOUR_SLACK_WEBHOOK_URL'
```

---

## Success Metrics

After 5-10 runs:
- ✅ Zero security incidents (no customer names, no credentials leaked)
- ✅ 90%+ PASS rate (most proposals pass without issues)
- ✅ False positive rate < 10% (warnings are valid)
- ✅ Average review time: 30-60 seconds
- ✅ Zero BLOCKING issues caused by agents (all caught before content generation)

**This implements defense-in-depth security and prevents low-quality outputs.**

---

## Notes

- **Customer Name List**: Maintain `data/context/customer_names.txt` with known customers (never commit to git)
- **Regular Updates**: Update maritime glossary and regulatory references quarterly
- **False Positives**: If certain warnings recur and are invalid, add to whitelist in validation scripts
- **Audit Trail**: All security events logged to `data/reports/security_audit.log` for compliance

---

## Related Documentation

- See `docs/SECURITY-GUIDELINES.md` for comprehensive security framework (Phase 3)
- See `docs/TROUBLESHOOTING.md` for QA review false positive handling (Phase 3)
- See `docs/SECURITY-GUIDELINES.md` for comprehensive security framework
- See Security & Data Safety section below for mandatory principles

---

## Reference: SEO/GEO/AEO Best Practice Standards

### SEO Standards
- Follow Google Search Essentials guidelines
- Implement schema markup (Organization, SoftwareApplication, Dataset, Article, FAQ)
- Optimize Core Web Vitals (LCP < 2.5s, INP < 200ms, CLS < 0.1)

### GEO/AEO Standards
- Direct answers in first 100 words
- Use lists/tables for scannable content
- Include authoritative citations (IMO, OFAC, Lloyd's List)
- Map entities to Wikidata IDs via Schema.org `sameAs`

### Data Safety (MANDATORY)
- **NEVER output specific customer names** — use generic descriptions ("a major commodity trader")
- **NEVER output non-public IMO numbers** — public ones OK with source citation
- **NEVER include internal Windward API keys, credentials, or proprietary data**
- Use aggregated statistics only in public content ("1,400+ vessels" not "1,427 vessels")

### Content Security Checklist
- [ ] No customer company names mentioned
- [ ] No non-public IMO numbers included
- [ ] No internal Windward metrics exposed
- [ ] No credentials/API keys in outputs
- [ ] External links validated (not phishing/malware)
- [ ] File paths sanitized (no `/Users/...`)
- [ ] Schema markup validated (no injection vulnerabilities)
