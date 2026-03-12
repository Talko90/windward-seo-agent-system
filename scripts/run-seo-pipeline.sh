#!/bin/bash
# Windward SEO Pipeline Runner
# Runs the full SEO pipeline via Claude Code CLI
# Scheduled: Sunday + Wednesday at 10:00 IST via launchd
#
# Usage:
#   ./scripts/run-seo-pipeline.sh           # Full run
#   ./scripts/run-seo-pipeline.sh targeted  # Targeted run (data + plan only)

set -euo pipefail

# Configuration
CLAUDE_CLI="/opt/homebrew/bin/claude"
PROJECT_DIR="/path/to/your/seo-project"
LOG_DIR="${PROJECT_DIR}/logs"
SLACK_WEBHOOK="YOUR_SLACK_WEBHOOK_URL"
RUN_MODE="${1:-full}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="${LOG_DIR}/pipeline_${TIMESTAMP}.log"

# Ensure log directory exists
mkdir -p "${LOG_DIR}"

# Log function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "${LOG_FILE}"
}

# Slack notification function
slack_notify() {
    local message="$1"
    curl -s -X POST -H 'Content-type: application/json' \
        --data "{\"text\":\"${message}\"}" \
        "${SLACK_WEBHOOK}" > /dev/null 2>&1 || log "WARNING: Slack notification failed"
}

# Pre-flight checks
log "=== Windward SEO Pipeline Starting ==="
log "Mode: ${RUN_MODE}"
log "Log: ${LOG_FILE}"

# Check Claude CLI exists
if [ ! -x "${CLAUDE_CLI}" ]; then
    log "ERROR: Claude CLI not found at ${CLAUDE_CLI}"
    slack_notify ":x: *SEO Pipeline Failed*\nClaude CLI not found at ${CLAUDE_CLI}"
    exit 1
fi

# Check network connectivity
if ! curl -s --max-time 5 https://api.anthropic.com > /dev/null 2>&1; then
    log "ERROR: No network connectivity (cannot reach api.anthropic.com)"
    slack_notify ":x: *SEO Pipeline Failed*\nNo network connectivity"
    exit 1
fi

# Check project directory exists
if [ ! -d "${PROJECT_DIR}" ]; then
    log "ERROR: Project directory not found: ${PROJECT_DIR}"
    exit 1
fi

# Send start notification
slack_notify ":rocket: *SEO Pipeline Starting*\nMode: ${RUN_MODE}\nTime: $(date '+%Y-%m-%d %H:%M IST')"

log "Pre-flight checks passed. Running pipeline..."

# Run the pipeline
cd "${PROJECT_DIR}"

PIPELINE_START=$(date +%s)

if "${CLAUDE_CLI}" --dangerously-skip-permissions -p "/seo-pipeline" >> "${LOG_FILE}" 2>&1; then
    PIPELINE_END=$(date +%s)
    DURATION=$(( (PIPELINE_END - PIPELINE_START) / 60 ))
    log "=== Pipeline completed successfully in ${DURATION} minutes ==="
    slack_notify ":white_check_mark: *SEO Pipeline Complete*\nDuration: ${DURATION} min\nMode: ${RUN_MODE}\nLog: logs/pipeline_${TIMESTAMP}.log"
else
    PIPELINE_END=$(date +%s)
    DURATION=$(( (PIPELINE_END - PIPELINE_START) / 60 ))
    EXIT_CODE=$?
    log "=== Pipeline FAILED with exit code ${EXIT_CODE} after ${DURATION} minutes ==="
    slack_notify ":x: *SEO Pipeline Failed*\nExit code: ${EXIT_CODE}\nDuration: ${DURATION} min\nCheck: logs/pipeline_${TIMESTAMP}.log"
fi

# Log rotation: keep last 20 runs
log "Rotating logs (keeping last 20)..."
cd "${LOG_DIR}"
ls -t pipeline_*.log 2>/dev/null | tail -n +21 | xargs rm -f 2>/dev/null || true

log "=== Pipeline runner finished ==="
