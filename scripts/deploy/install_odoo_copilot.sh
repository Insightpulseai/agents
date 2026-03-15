#!/bin/bash
# =============================================================================
# Install ipai_odoo_copilot_bridge Module in Odoo
# =============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"

ENVIRONMENT="${ENVIRONMENT:-staging}"
ODOO_URL="${COPILOT_ODOO_BASE_URL:-http://localhost:8069}"
ODOO_DB="${ODOO_DB:-odoo}"
ODOO_ADMIN="${ODOO_ADMIN_PASSWORD:-admin}"
MODULE_NAME="ipai_odoo_copilot_bridge"

DRY_RUN="${1:-}"

log()  { echo "[$(date +%H:%M:%S)] $*"; }
fail() { log "ERROR: $*" >&2; exit 1; }

# ---------------------------------------------------------------------------
# Step 1 — Verify module source exists
# ---------------------------------------------------------------------------
verify_module() {
    local module_path="$PROJECT_ROOT/odoo/addons/$MODULE_NAME"
    [[ -d "$module_path" ]]             || fail "Module not found: $module_path"
    [[ -f "$module_path/__manifest__.py" ]] || fail "Missing __manifest__.py"
    [[ -f "$module_path/__init__.py" ]]     || fail "Missing __init__.py"
    log "Module source verified: $module_path"
}

# ---------------------------------------------------------------------------
# Step 2 — Check Odoo is reachable
# ---------------------------------------------------------------------------
check_odoo() {
    log "Checking Odoo at $ODOO_URL..."
    local status
    status=$(curl -sf -o /dev/null -w "%{http_code}" "$ODOO_URL/web/login" 2>/dev/null || echo "000")

    if [[ "$status" == "200" || "$status" == "303" ]]; then
        log "Odoo is reachable (HTTP $status)"
    else
        fail "Odoo not reachable at $ODOO_URL (HTTP $status)"
    fi
}

# ---------------------------------------------------------------------------
# Step 3 — Update module list + install
# ---------------------------------------------------------------------------
install_module() {
    log "Installing module $MODULE_NAME..."

    if [[ "$DRY_RUN" == "--dry-run" ]]; then
        log "[DRY RUN] Would install $MODULE_NAME on $ODOO_DB"
        return 0
    fi

    # Method A: Docker exec (if running in container)
    if docker ps --format '{{.Names}}' 2>/dev/null | grep -q odoo; then
        local container
        container=$(docker ps --format '{{.Names}}' | grep odoo | head -1)
        log "Found Odoo container: $container"

        # Update module list
        docker exec "$container" \
            odoo --no-http -d "$ODOO_DB" --update base --stop-after-init 2>/dev/null || true

        # Install module
        docker exec "$container" \
            odoo --no-http -d "$ODOO_DB" -i "$MODULE_NAME" --stop-after-init

        log "Module installed via Docker exec"
        return 0
    fi

    # Method B: XML-RPC (works remotely)
    log "Installing via XML-RPC..."
    python3 - <<XMLRPC_EOF
import xmlrpc.client
import sys

url = "$ODOO_URL"
db = "$ODOO_DB"
password = "$ODOO_ADMIN"

common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
uid = common.authenticate(db, "admin", password, {})
if not uid:
    print("ERROR: Authentication failed", file=sys.stderr)
    sys.exit(1)

models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")

# Update module list
models.execute_kw(db, uid, password, "ir.module.module", "update_list", [])
print("Module list updated")

# Search for the module
module_ids = models.execute_kw(
    db, uid, password, "ir.module.module", "search",
    [[("name", "=", "$MODULE_NAME")]]
)

if not module_ids:
    print("ERROR: Module $MODULE_NAME not found. Is the addons path configured?", file=sys.stderr)
    sys.exit(1)

module = models.execute_kw(
    db, uid, password, "ir.module.module", "read",
    [module_ids, ["name", "state"]]
)[0]

print(f"Module state: {module['state']}")

if module["state"] == "installed":
    # Upgrade
    models.execute_kw(db, uid, password, "ir.module.module", "button_immediate_upgrade", [module_ids])
    print("Module upgraded successfully")
elif module["state"] in ("uninstalled", "to install"):
    # Install
    models.execute_kw(db, uid, password, "ir.module.module", "button_immediate_install", [module_ids])
    print("Module installed successfully")
else:
    print(f"Module in state '{module['state']}' — manual action may be required")
XMLRPC_EOF

    log "Module installation complete"
}

# ---------------------------------------------------------------------------
# Step 4 — Verify installation
# ---------------------------------------------------------------------------
verify_install() {
    log "Verifying installation..."

    if [[ "$DRY_RUN" == "--dry-run" ]]; then
        log "[DRY RUN] Would verify module installation"
        return 0
    fi

    # Check the copilot endpoint is responding
    local status
    status=$(curl -sf -o /dev/null -w "%{http_code}" \
        -X POST "$ODOO_URL/ipai/copilot/chat" \
        -H "Content-Type: application/json" \
        -d '{"message": "ping", "session_id": null}' 2>/dev/null || echo "000")

    if [[ "$status" == "200" ]]; then
        log "Copilot endpoint responding (HTTP 200)"
    elif [[ "$status" == "403" || "$status" == "401" ]]; then
        log "Copilot endpoint exists but requires auth (HTTP $status) — expected for unauthenticated test"
    else
        log "WARN: Copilot endpoint returned HTTP $status — check Odoo logs"
    fi
}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
main() {
    log "=== Install Odoo Copilot Bridge: $MODULE_NAME ==="
    log "Environment: $ENVIRONMENT"
    log "Odoo URL:    $ODOO_URL"
    log "Database:    $ODOO_DB"
    [[ "$DRY_RUN" == "--dry-run" ]] && log "MODE: DRY RUN"
    echo ""

    verify_module
    check_odoo
    install_module
    verify_install

    echo ""
    log "=== Installation complete ==="
    log ""
    log "Verify in Odoo:"
    log "  1. Settings > Technical > Modules > Search '$MODULE_NAME'"
    log "  2. Check Copilot menu under 'AI Copilot'"
    log "  3. Test: curl -X POST $ODOO_URL/ipai/copilot/chat -d '{\"message\":\"hello\"}'"
}

main "$@"
