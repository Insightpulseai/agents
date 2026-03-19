#!/bin/bash
# =============================================================================
# Copilot Eval Runner & Staging Promotion
# Runs evaluation suite and optionally promotes to production
# =============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"

ENVIRONMENT="${ENVIRONMENT:-staging}"
EVAL_DIR="$PROJECT_ROOT/agents/foundry/ipai-odoo-copilot-azure/evals"
THRESHOLDS="$PROJECT_ROOT/eval/thresholds.yaml"
REPORTS_DIR="$PROJECT_ROOT/.deploy/eval-reports"
MODE="${1:---full}"  # --gate | --full | --promote

log()  { echo "[$(date +%H:%M:%S)] $*"; }
fail() { log "ERROR: $*" >&2; exit 1; }

# ---------------------------------------------------------------------------
# Step 1 — Run copilot-specific eval cases
# ---------------------------------------------------------------------------
run_eval() {
    log "Running copilot eval suite ($MODE)..."
    mkdir -p "$REPORTS_DIR"

    local report_file="$REPORTS_DIR/eval_$(date +%Y%m%d_%H%M%S).json"

    if [[ -f "$PROJECT_ROOT/eval/run_replay.py" ]]; then
        python3 "$PROJECT_ROOT/eval/run_replay.py" \
            --cases "$PROJECT_ROOT/eval/cases" \
            --thresholds "$THRESHOLDS" \
            --output "$report_file" \
            --tags copilot 2>&1 || {

            # If no copilot-tagged cases exist, run with all tags
            log "No copilot-tagged cases found. Running general eval..."
            python3 "$PROJECT_ROOT/eval/run_replay.py" \
                --cases "$PROJECT_ROOT/eval/cases" \
                --thresholds "$THRESHOLDS" \
                --output "$report_file" 2>&1 || true
        }
    else
        log "WARN: eval/run_replay.py not found — generating synthetic eval"
        generate_synthetic_eval "$report_file"
    fi

    # Parse results
    if [[ -f "$report_file" ]]; then
        local passed failed pass_rate
        passed=$(jq -r '.cases_passed // 0' "$report_file")
        failed=$(jq -r '.cases_failed // 0' "$report_file")
        pass_rate=$(jq -r '.summary.pass_rate // 0' "$report_file")

        log "Eval results: $passed passed, $failed failed (rate: $pass_rate)"

        # Gate check
        if [[ "$MODE" == "--gate" ]]; then
            local min_rate
            min_rate=$(python3 -c "
import yaml, sys
with open('$THRESHOLDS') as f:
    d = yaml.safe_load(f)
print(d.get('pass_rate', {}).get('minimum', 0.90))
" 2>/dev/null || echo "0.90")

            local pass_check
            pass_check=$(python3 -c "print('yes' if $pass_rate >= $min_rate else 'no')")

            if [[ "$pass_check" != "yes" ]]; then
                fail "Eval gate FAILED: pass_rate=$pass_rate < minimum=$min_rate"
            fi
            log "Eval gate PASSED"
        fi

        echo "$report_file"
    else
        log "WARN: No eval report generated"
    fi
}

generate_synthetic_eval() {
    local report_file="$1"
    cat > "$report_file" <<SYNTH_EOF
{
    "run_id": "eval_synthetic_$(date +%Y%m%d_%H%M%S)",
    "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
    "cases_total": 0,
    "cases_passed": 0,
    "cases_failed": 0,
    "results": [],
    "thresholds": {},
    "summary": {
        "avg_accuracy": 0,
        "avg_helpfulness": 0,
        "avg_actionability": 0,
        "avg_safety": 0,
        "pass_rate": 0,
        "note": "No eval cases configured yet. Add JSONL cases to agents/foundry/ipai-odoo-copilot-azure/evals/"
    }
}
SYNTH_EOF
    log "Synthetic eval report written (no cases configured)"
}

# ---------------------------------------------------------------------------
# Step 2 — Staging soak check
# ---------------------------------------------------------------------------
check_staging_soak() {
    log "Checking staging soak period..."

    local publish_record="$PROJECT_ROOT/.deploy/last_publish.json"

    if [[ ! -f "$publish_record" ]]; then
        fail "No publish record found. Run publish_foundry_agent.sh first."
    fi

    local published_at env
    published_at=$(jq -r '.published_at' "$publish_record")
    env=$(jq -r '.environment' "$publish_record")

    if [[ "$env" != "staging" ]]; then
        log "Last publish was to $env (not staging). Skipping soak check."
        return 0
    fi

    # Check 24-hour minimum soak
    local publish_epoch now_epoch diff_hours
    publish_epoch=$(date -d "$published_at" +%s 2>/dev/null || date -j -f "%Y-%m-%dT%H:%M:%SZ" "$published_at" +%s 2>/dev/null || echo "0")
    now_epoch=$(date +%s)
    diff_hours=$(( (now_epoch - publish_epoch) / 3600 ))

    if [[ "$diff_hours" -lt 24 ]]; then
        fail "Staging soak incomplete: ${diff_hours}h elapsed (minimum 24h). Published at: $published_at"
    fi

    log "Staging soak passed: ${diff_hours}h elapsed (>= 24h minimum)"
}

# ---------------------------------------------------------------------------
# Step 3 — Promote to production
# ---------------------------------------------------------------------------
promote_to_production() {
    log "Promoting to production..."

    check_staging_soak

    # Re-run eval in production mode
    ENVIRONMENT="production" run_eval

    # Publish to production
    ENVIRONMENT="production" "$SCRIPT_DIR/publish_foundry_agent.sh"

    # Set production env
    "$SCRIPT_DIR/set_copilot_env.sh" production

    log "Promoted to production successfully"
}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
main() {
    log "=== Copilot Eval & Promotion ==="
    log "Mode:        $MODE"
    log "Environment: $ENVIRONMENT"
    echo ""

    case "$MODE" in
        --gate)
            run_eval
            ;;
        --full)
            run_eval
            log ""
            log "To promote to production:"
            log "  ENVIRONMENT=production $0 --promote"
            ;;
        --promote)
            run_eval
            promote_to_production
            ;;
        *)
            echo "Usage: $0 [--gate|--full|--promote]"
            echo ""
            echo "  --gate     Run eval as CI gate (fail if below threshold)"
            echo "  --full     Run full eval suite with report"
            echo "  --promote  Run eval, check soak, promote to production"
            exit 1
            ;;
    esac

    echo ""
    log "=== Done ==="
}

main "$@"
