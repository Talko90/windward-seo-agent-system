# /seo-health-check - System Diagnostics Agent

**Purpose**: Validates that the SEO agent system is properly configured and all dependencies are working before running workflows.

**When to Run**:
- Before first `/seo-pipeline` run (setup validation)
- Weekly on Monday mornings (proactive health check)
- After MCP server configuration changes
- When experiencing workflow failures

**Output**: Health report with pass/fail status for each component and actionable fix recommendations.

---

## What This Agent Checks

1. File System Structure
2. Data Freshness & Availability
3. MCP Connectivity
4. External Integrations
5. Agent Skills Availability
6. Configuration Correctness

---

## Health Check Workflow

### Check 1: File System Structure

**Validates**: All required directories and critical files exist

```bash
required_dirs=(
    "data/master" "data/proposals" "data/raw"
    "data/reports" "data/drafts" "data/context"
    "cache" "scripts" ".claude/commands"
)

for dir in "${required_dirs[@]}"; do
    [ -d "$dir" ] && echo "✅ $dir" || { echo "❌ MISSING: $dir"; recommendations+=("mkdir -p $dir"); }
done

critical_files=(
    "CLAUDE.md" "skills.md"
    "data/master/action_queue.json"
    "data/master/keywords_db.json"
    "data/master/content_index.json"
)

for file in "${critical_files[@]}"; do
    [ -f "$file" ] && echo "✅ $file" || { echo "❌ MISSING: $file"; recommendations+=("File missing: $file"); }
done
```

**Status**: PASS if all directories exist, WARNING if non-critical files missing, FAIL if master databases missing

---

### Check 2: Data Freshness & Availability

**Validates**: Data is recent enough for analysis. Freshness threshold: PASS < 7 days, WARNING 7-30 days, FAIL > 30 days or missing.

For each data source below, check existence, compute age in days, and report status:

| Source | File | Metric |
|--------|------|--------|
| GSC | `data/raw/gsc_dump.csv` | Age in days |
| Sitemap | `data/raw/sitemap_urls.json` | Age in days |
| Content Index | `data/master/content_index.json` | Page count via `jq '.pages \| length'` |

```bash
# Helper: check_freshness <file> <label>
check_freshness() {
    local file=$1 label=$2
    if [ -f "$file" ]; then
        local age=$(( ($(date +%s) - $(stat -f %m "$file")) / 86400 ))
        [ $age -le 7 ] && echo "✅ $label fresh ($age days)" || echo "⚠️ $label stale ($age days)"
    else
        echo "❌ $label missing"
        recommendations+=("Run /seo-data to fetch $label")
    fi
}

check_freshness "data/raw/gsc_dump.csv" "GSC data"
check_freshness "data/raw/sitemap_urls.json" "Sitemap data"

# Content index: check existence and page count
if [ -f "data/master/content_index.json" ]; then
    content_count=$(jq '.pages | length' data/master/content_index.json)
    [ $content_count -gt 0 ] && echo "✅ Content index ($content_count pages)" || echo "⚠️ Content index empty"
else
    echo "❌ Content index missing"
fi
```

---

### Check 3: MCP Server Connectivity

**Validates**: MCP servers are configured and responsive

#### A. Check MCP Configuration File

```bash
if [ -f ".mcp.json" ]; then
    echo "✅ MCP config file exists"

    # Google Sheets MCP
    if jq -e '.mcpServers."google-sheets"' .mcp.json > /dev/null 2>&1; then
        echo "✅ Google Sheets MCP configured"
        cred_path=$(jq -r '.mcpServers."google-sheets".env.GOOGLE_SHEETS_CREDENTIALS_PATH' .mcp.json)
        [ -f "$cred_path" ] && echo "✅ Credentials file exists" || { echo "❌ Credentials missing: $cred_path"; recommendations+=("Place service account JSON at: $cred_path"); }
    else
        echo "⚠️ Google Sheets MCP not configured"
        recommendations+=("Configure Google Sheets MCP in .mcp.json (see CLAUDE.md)")
    fi

    # BigQuery MCP (optional)
    jq -e '.mcpServers."bigquery"' .mcp.json > /dev/null 2>&1 && echo "✅ BigQuery MCP configured" || echo "ℹ️ BigQuery MCP not configured (optional)"
else
    echo "⚠️ .mcp.json not found"
    recommendations+=("Create .mcp.json in project root (see MCP Configuration section below)")
fi
```

#### B. Test MCP Server Connectivity

Test each configured MCP server by making a simple read call:

- **Google Sheets MCP**: Call `list_sheets` on the dashboard spreadsheet (`YOUR_GOOGLE_SHEETS_ID`). PASS if response includes "Action Queue".
- **BigQuery MCP** (optional): Call `list-tables`. PASS if no error in response.

**Status**: PASS if all configured MCPs respond, WARNING if unconfigured (optional), FAIL if configured but not responding

---

### Check 4: External Integrations

#### A. Slack Webhook

Send a test message via the Slack Notification Protocol (see CLAUDE.md). Use payload: `{"text":"Health check test from SEO system"}`. PASS if response contains "ok".

#### B. Python Scripts

```bash
if command -v python3 &> /dev/null; then
    echo "✅ Python 3 available"

    # Check dependencies from requirements.txt
    if [ -f "scripts/requirements.txt" ]; then
        missing_deps=0
        while IFS= read -r package; do
            pkg_name=$(echo "$package" | cut -d'=' -f1 | cut -d'>' -f1 | cut -d'<' -f1)
            python3 -c "import $pkg_name" 2>/dev/null || { echo "❌ Missing: $pkg_name"; missing_deps=$((missing_deps + 1)); }
        done < "scripts/requirements.txt"
        [ $missing_deps -eq 0 ] && echo "✅ All Python deps installed" || recommendations+=("pip3 install -r scripts/requirements.txt")
    fi

    # Google API credentials
    [ -f "scripts/credentials.json" ] && echo "✅ Google API credentials found" || echo "⚠️ Google API credentials missing (MCP or manual exports required)"
else
    echo "⚠️ Python 3 not available (MCP or manual exports required)"
fi
```

**Status**: PASS if all integrations work, WARNING if optional features unavailable, FAIL if critical integration broken

---

### Check 5: Agent Skills Availability

**Validates**: All agent skills are present

```bash
required_skills=(
    "seo-data" "seo-keywords" "seo-competitors" "seo-geo"
    "seo-technical" "seo-plan" "seo-content" "seo-links"
    "seo-learning" "seo-pipeline" "seo-review" "seo-health-check" "seo-agents"
)

missing_skills=0
for skill in "${required_skills[@]}"; do
    [ -f ".claude/commands/${skill}.md" ] && echo "✅ /$skill" || { echo "❌ MISSING: /$skill"; missing_skills=$((missing_skills + 1)); }
done
echo "$((${#required_skills[@]} - missing_skills))/${#required_skills[@]} skills present"
```

**Status**: FAIL if core skills missing (seo-data, seo-plan, seo-pipeline), WARNING if optional skills missing

---

### Check 6: Configuration Correctness

#### A. Validate CLAUDE.md

Check that these required sections exist in CLAUDE.md (grep for `## <section_name>`):

- Architecture
- Execution Rules
- Security
- Slack
- Shared Agent Protocols

Report count of missing sections. PASS if none missing, WARNING if outdated.

#### B. Validate skills.md

```bash
if [ -f "skills.md" ]; then
    skill_entries=$(grep -c "^###" skills.md)
    skills_age=$(( ($(date +%s) - $(stat -f %m "skills.md")) / 86400 ))
    echo "✅ skills.md ($skill_entries entries, $skills_age days old)"
    [ $skills_age -gt 30 ] && recommendations+=("Run /seo-learning to capture recent learnings")
else
    echo "❌ skills.md missing"
    recommendations+=("Initialize skills.md for continuous learning")
fi
```

---

## Health Report Output

Save two files:

### JSON Report → `data/reports/health_check_[timestamp].json`

```json
{
  "check_date": "ISO-8601 timestamp",
  "overall_status": "PASS | WARNING | FAIL",
  "checks": {
    "file_system":           { "status": "...", "details": "...", "score": 0-100 },
    "data_freshness":        { "status": "...", "details": "...", "score": 0-100 },
    "mcp_connectivity":      { "status": "...", "details": "...", "score": 0-100 },
    "external_integrations": { "status": "...", "details": "...", "score": 0-100 },
    "agent_skills":          { "status": "...", "details": "...", "score": 0-100 },
    "configuration":         { "status": "...", "details": "...", "score": 0-100 }
  },
  "recommendations": [],
  "system_info": {
    "project_root": "~/Claude Main",
    "python_version": "...",
    "mcp_servers_configured": [],
    "total_pages_indexed": 0,
    "total_keywords_tracked": 0,
    "last_pipeline_run": "ISO-8601 timestamp"
  }
}
```

### Human-Readable Summary → `data/reports/health_check_[timestamp]_summary.txt`

Format: Overall status header, then each component with sub-details indented, followed by recommendations list and next check date.

---

## Usage

```bash
/seo-health-check           # Run full health check
cat data/reports/health_check_*_summary.txt  # View results
# If FAIL → fix issues using recommendations → re-run
```

## Workflow Integration

- **Monday mornings**: Run before `/seo-pipeline`. Proceed only on PASS.
- **After config changes**: Always re-run after modifying `.mcp.json` or moving files.
- **On failures**: Run as first diagnostic step.
- **Safe to run anytime**: Read-only, never modifies data.

---

## Error Handling

Follow Error Handling Protocol from CLAUDE.md (Rule 3). If the health check itself fails, log to `data/reports/health_check_errors.log` and report "HEALTH CHECK FAILED - manual inspection required".

---

## Slack Notification

Follow Slack Notification Protocol from CLAUDE.md. Use header emoji `:hospital:`, include overall status, component pass count, data freshness, and MCP status. Link to full report file path.

---

## Related Documentation

- `docs/TROUBLESHOOTING.md` - Fixing common issues flagged by health check
- `docs/MCP-SETUP-REFERENCE.md` - Resolving MCP configuration issues
- See MCP Configuration Reference section below for exact config syntax

---

## Reference: MCP Configuration

**Configuration file location:** `.mcp.json` in project root (NOT `settings.json`, NOT `.claude/settings.json`)

**Google Sheets MCP Configuration:**
```json
{
  "mcpServers": {
    "google-sheets": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-google-sheets"],
      "env": {
        "GOOGLE_SHEETS_CREDENTIALS_PATH": "~/Claude Main/scripts/google-sheets-service-account.json"
      }
    }
  }
}
```

**Environment Variables (EXACT NAMES):**
- `GOOGLE_SHEETS_CREDENTIALS_PATH` - Absolute path to service account JSON

### Common Mistakes

| Mistake | Correct Approach |
|---------|------------------|
| Config in `~/.claude/settings.json` | Use `.mcp.json` in project root |
| Relative path for credentials | Use absolute path |
| Wrong env var name | Use `GOOGLE_SHEETS_CREDENTIALS_PATH` exactly |
| Forgot to share spreadsheet | Share with service account email |

### Troubleshooting

1. Check config: `ls -la .mcp.json && cat .mcp.json | python3 -m json.tool`
2. Verify credentials path exists and is valid JSON
3. Verify spreadsheet shared with service account email (find in credentials JSON `client_email` field)
4. Test: Use `mcp__google-sheets__list_sheets` with spreadsheet ID
