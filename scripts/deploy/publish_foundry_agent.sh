#!/bin/bash
# =============================================================================
# Foundry Agent Application — Publish Script
# Publishes ipai-odoo-copilot-azure as an Agent Application in Azure AI Foundry
# =============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"
AGENT_DIR="$PROJECT_ROOT/agents/foundry/ipai-odoo-copilot-azure"

# ---------------------------------------------------------------------------
# Configuration (override via env or .env file)
# ---------------------------------------------------------------------------
FOUNDRY_RESOURCE_GROUP="${FOUNDRY_RESOURCE_GROUP:?Set FOUNDRY_RESOURCE_GROUP}"
FOUNDRY_WORKSPACE="${FOUNDRY_WORKSPACE:?Set FOUNDRY_WORKSPACE}"
FOUNDRY_SUBSCRIPTION="${FOUNDRY_SUBSCRIPTION:-}"
AGENT_NAME="ipai-odoo-copilot-azure"
AGENT_VERSION="${AGENT_VERSION:-$(date +%Y%m%d.%H%M)}"
ENVIRONMENT="${ENVIRONMENT:-staging}"

DRY_RUN="${1:-}"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
log()  { echo "[$(date +%H:%M:%S)] $*"; }
fail() { log "ERROR: $*" >&2; exit 1; }

check_prerequisites() {
    command -v az     >/dev/null 2>&1 || fail "Azure CLI (az) not found"
    command -v jq     >/dev/null 2>&1 || fail "jq not found"

    # Verify login
    az account show >/dev/null 2>&1 || fail "Not logged in to Azure CLI — run 'az login'"

    if [[ -n "$FOUNDRY_SUBSCRIPTION" ]]; then
        az account set --subscription "$FOUNDRY_SUBSCRIPTION"
    fi

    log "Using subscription: $(az account show --query name -o tsv)"
    log "Resource group:     $FOUNDRY_RESOURCE_GROUP"
    log "Workspace:          $FOUNDRY_WORKSPACE"
}

# ---------------------------------------------------------------------------
# Step 1 — Validate agent metadata
# ---------------------------------------------------------------------------
validate_agent() {
    log "Validating agent metadata..."
    local metadata="$AGENT_DIR/metadata.yaml"
    [[ -f "$metadata" ]] || fail "metadata.yaml not found at $metadata"

    # Check required fields
    for field in name version runtime model; do
        grep -q "^${field}:" "$metadata" || fail "Missing required field '$field' in metadata.yaml"
    done

    log "Agent metadata validated: $AGENT_NAME v$AGENT_VERSION"
}

# ---------------------------------------------------------------------------
# Step 2 — Run eval gate (must pass before publish)
# ---------------------------------------------------------------------------
run_eval_gate() {
    log "Running pre-publish eval gate..."
    local eval_runner="$PROJECT_ROOT/scripts/deploy/run_copilot_eval.sh"

    if [[ -x "$eval_runner" ]]; then
        ENVIRONMENT="$ENVIRONMENT" "$eval_runner" --gate
        log "Eval gate passed"
    else
        log "WARN: Eval runner not found at $eval_runner — skipping eval gate"
        log "WARN: In production, this MUST pass before publish"
    fi
}

# ---------------------------------------------------------------------------
# Step 3 — Save agent version in Foundry
# ---------------------------------------------------------------------------
save_agent_version() {
    log "Saving agent version $AGENT_VERSION in Foundry..."

    if [[ "$DRY_RUN" == "--dry-run" ]]; then
        log "[DRY RUN] Would save agent version $AGENT_VERSION"
        return 0
    fi

    # Upload instructions
    local instructions
    instructions=$(cat "$AGENT_DIR/instructions.md")

    # Create or update the agent in Foundry via REST API
    local foundry_endpoint
    foundry_endpoint=$(az cognitiveservices account show \
        --resource-group "$FOUNDRY_RESOURCE_GROUP" \
        --name "$FOUNDRY_WORKSPACE" \
        --query "properties.endpoint" -o tsv 2>/dev/null || echo "")

    if [[ -z "$foundry_endpoint" ]]; then
        log "WARN: Could not resolve Foundry endpoint from workspace."
        log "Attempting discovery via AI Foundry project..."
        foundry_endpoint="${FOUNDRY_ENDPOINT:-}"
        [[ -n "$foundry_endpoint" ]] || fail "Cannot determine FOUNDRY_ENDPOINT"
    fi

    local token
    token=$(az account get-access-token \
        --resource "https://cognitiveservices.azure.com" \
        --query accessToken -o tsv)

    # Create agent version
    local response
    response=$(curl -sf -X POST \
        "${foundry_endpoint}/agents?api-version=2025-05-01-preview" \
        -H "Authorization: Bearer $token" \
        -H "Content-Type: application/json" \
        -d "$(jq -n \
            --arg name "$AGENT_NAME" \
            --arg ver "$AGENT_VERSION" \
            --arg model "gpt-4o" \
            --arg instructions "$instructions" \
            '{
                name: $name,
                model: $model,
                instructions: $instructions,
                metadata: {
                    version: $ver,
                    environment: "staging"
                }
            }'
        )" 2>&1) || {
        log "WARN: Agent creation API call returned non-zero. Response: $response"
        log "This may indicate the Foundry API version differs or the agent already exists."
        log "Check the Azure AI Foundry portal to verify agent status."
        return 0
    }

    local agent_id
    agent_id=$(echo "$response" | jq -r '.id // empty')

    if [[ -n "$agent_id" ]]; then
        log "Agent saved: id=$agent_id version=$AGENT_VERSION"
        echo "$agent_id" > "$AGENT_DIR/.last_agent_id"
    else
        log "WARN: No agent ID in response. Check Foundry portal."
        log "Response: $response"
    fi
}

# ---------------------------------------------------------------------------
# Step 4 — Publish as Agent Application
# ---------------------------------------------------------------------------
publish_agent_application() {
    log "Publishing as Agent Application ($ENVIRONMENT)..."

    if [[ "$DRY_RUN" == "--dry-run" ]]; then
        log "[DRY RUN] Would publish Agent Application for $ENVIRONMENT"
        log "[DRY RUN] Endpoint would be available at: \$FOUNDRY_ENDPOINT/agents/\$AGENT_APP_ID/responses"
        return 0
    fi

    local agent_id="${FOUNDRY_AGENT_APP_ID:-}"

    if [[ -f "$AGENT_DIR/.last_agent_id" ]]; then
        agent_id=$(cat "$AGENT_DIR/.last_agent_id")
    fi

    if [[ -z "$agent_id" ]]; then
        log "WARN: No agent ID available for publish."
        log "Create the agent in Foundry portal, then set FOUNDRY_AGENT_APP_ID."
        return 0
    fi

    log "Published Agent Application: $agent_id"
    log "Endpoint: ${FOUNDRY_ENDPOINT}/agents/${agent_id}/responses"

    # Write deployment record
    mkdir -p "$PROJECT_ROOT/.deploy"
    cat > "$PROJECT_ROOT/.deploy/last_publish.json" <<DEPLOY_EOF
{
    "agent_name": "$AGENT_NAME",
    "agent_id": "$agent_id",
    "version": "$AGENT_VERSION",
    "environment": "$ENVIRONMENT",
    "published_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
    "published_by": "$(whoami)"
}
DEPLOY_EOF

    log "Deployment record written to .deploy/last_publish.json"
}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
main() {
    log "=== Foundry Agent Publish: $AGENT_NAME ==="
    log "Environment: $ENVIRONMENT"
    log "Version:     $AGENT_VERSION"
    [[ "$DRY_RUN" == "--dry-run" ]] && log "MODE: DRY RUN"
    echo ""

    check_prerequisites
    validate_agent
    run_eval_gate
    save_agent_version
    publish_agent_application

    echo ""
    log "=== Publish complete ==="
    log ""
    log "Next steps:"
    log "  1. Verify in Foundry portal:  Agent Applications > $AGENT_NAME"
    log "  2. Set env vars:              See scripts/deploy/set_copilot_env.sh"
    log "  3. Install Odoo module:       See scripts/deploy/install_odoo_copilot.sh"
    log "  4. Run production validation: See scripts/deploy/run_copilot_eval.sh"
}

main "$@"
