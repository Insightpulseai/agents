# GitHub App Authentication Setup (pulser-hub)

**Purpose**: Replace PAT-based automation with GitHub App installation tokens for secure, org-wide automation.

**Current Status**: GitHub App `pulser-hub` (app_id: 2191216) exists but is not yet installed to Insightpulseai-net organization.

---

## 0. Architecture Overview

```
GitHub → pulser-hub App
   ↓ Webhooks
n8n.insightpulseai.net/webhook/github/pulser-hub
   ↓ Signature validation + event routing
Supabase ops.runs / ops.run_events
   ↓ Control Room
mcp.insightpulseai.net (UI/API)
```

**Clean domain separation**:
- `mcp.insightpulseai.net` - Human-facing UI/API, OAuth callback (if needed), GitHub App homepage
- `n8n.insightpulseai.net` - Inbound webhooks, job dispatch, automation orchestration

---

## 1. GitHub App Configuration (Settings Page)

### A) URLs

**Homepage URL** (human-facing):
```
https://mcp.insightpulseai.net
```

**Webhook URL** (events receiver):
```
https://n8n.insightpulseai.net/webhook/github/pulser-hub
```

**Webhook Secret**: Rotate and store in n8n credentials/env only

**Callback URL** (optional - only if OAuth login needed):
```
https://mcp.insightpulseai.net/oauth/github/callback
```

**Recommendation**: Disable "Request user authorization during installation" unless you need "Sign in with GitHub" UI flow.

### B) Permissions (Minimum Required Set)

**Repository Permissions**:
- **Contents**: Read & write (commit/PR branches)
- **Pull requests**: Read & write
- **Issues**: Read & write
- **Checks**: Read-only (CI results)
- **Actions**: Read-only (workflow runs)
- **Metadata**: Read-only (always)

**Organization Permissions**:
- **Members**: Read-only (optional - only if mapping org users)
- **Projects**: Read & write (⚠️ **REQUIRED** for Projects v2 automation)

**Subscribe to Events** (webhooks):
- ✅ issues
- ✅ pull_request
- ✅ push
- ✅ workflow_run
- ✅ check_suite / check_run (optional but useful)
- ✅ project_items (ONLY if automating Projects v2)

---

## 2. Secrets Storage (Environment Variables)

### For Supabase Edge Functions / Control Room Backend

```bash
# GitHub App authentication
GITHUB_APP_ID=2191216
GITHUB_APP_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
GITHUB_APP_INSTALLATION_ID="<installation_id>"  # From installation step
GITHUB_WEBHOOK_SECRET="<webhook_secret>"

# Optional OAuth (only if used)
GITHUB_CLIENT_ID=Iv23liwGL7fnYySPPAjS
GITHUB_CLIENT_SECRET="<client_secret>"

# Targets
GITHUB_ORG=Insightpulseai-net
```

### For n8n

Store in n8n credentials/environment:
```bash
GITHUB_APP_WEBHOOK_SECRET="<webhook_secret>"
# Optional: Supabase service role key if n8n writes to ops schema
SUPABASE_SERVICE_ROLE_KEY="<key>"
```

### For GitHub Actions (per repo/org secrets)

```bash
PULSER_APP_ID=2191216
PULSER_APP_PRIVATE_KEY="<PEM content>"
```

---

## 3. n8n Webhook Workflow

### Endpoint

Create **Webhook** node at: `POST /webhook/github/pulser-hub`

### Step 1: Verify Signature (REQUIRED)

**Function node** after webhook:

```javascript
const crypto = require("crypto");

const secret = $env.GITHUB_APP_WEBHOOK_SECRET;
const sig = $headers["x-hub-signature-256"];
const body = JSON.stringify($json);

if (!sig || !secret) throw new Error("Missing signature or secret");

const hmac = crypto.createHmac("sha256", secret).update(body).digest("hex");
const expected = `sha256=${hmac}`;

if (sig !== expected) throw new Error("Invalid signature");

return $input.all();
```

### Step 2: Normalize Event Type

**Function node** to extract event metadata:

```javascript
const event = $headers["x-github-event"];
const action = $json.action || "";
return [{ json: { event, action, payload: $json } }];
```

### Step 3: Route by Event Type

**Switch node** routing:

- **pull_request** (action: opened/synchronize/closed)
  - Auto-add to Delivery Ops project
  - Update status based on CI

- **issues** (action: opened/labeled)
  - Auto-label based on content
  - Auto-add to Learning Ops if "learning" label

- **workflow_run** (action: completed)
  - Log to ops.run_events
  - Notify on failure

- **project_items** (action: created/updated)
  - Sync project status changes
  - Track progress metrics

---

## 4. GitHub Actions Workflow Integration

### Generate Installation Token at Runtime

Replace static `PROJECTS_TOKEN` with dynamic App token:

```yaml
name: Auto-add to Projects
on:
  issues:
    types: [opened, labeled]
  pull_request:
    types: [opened, synchronize]

jobs:
  add_to_project:
    runs-on: ubuntu-latest
    steps:
      - name: Generate GitHub App token
        id: app-token
        uses: actions/create-github-app-token@v1
        with:
          app-id: ${{ vars.PULSER_APP_ID }}
          private-key: ${{ secrets.PULSER_APP_PRIVATE_KEY }}
          owner: Insightpulseai-net

      - name: Add to project
        env:
          GH_TOKEN: ${{ steps.app-token.outputs.token }}
          ORG: Insightpulseai-net
        run: |
          # Use $GH_TOKEN instead of secrets.PROJECTS_TOKEN
          ./scripts/gh_projects_add_issue.sh "$PROJECT_TITLE" "$ISSUE_URL" "$STATUS"
```

### Benefits Over PAT

✅ Scoped to org/repo (not user-wide)
✅ Auto-revoked on app uninstall
✅ Auditable via GitHub App activity log
✅ No expiration management (tokens are ephemeral)
✅ Follows least-privilege principle

---

## 5. Migration from PAT to GitHub App

### Current State (PAT-based)

6 repos using `PROJECTS_TOKEN` secret: `ghp_REDACTED_SEE_GITHUB_SECRETS`

**Repos**:
- pulser-agent-framework
- pulser-mcp
- tbwa-fin-ops
- odoomation
- landing.io
- demo-repository

### Migration Steps

**Phase 1: GitHub App Setup**
1. ✅ GitHub App created (app_id: 2191216)
2. ⏳ Install app to Insightpulseai-net organization
3. ⏳ Configure webhook URL and secret
4. ⏳ Set permissions (Projects: Read & write, Contents: Read & write, etc.)
5. ⏳ Generate private key and store securely

**Phase 2: Organization Secrets**
```bash
# Set org-level variables and secrets
gh variable set PULSER_APP_ID --org Insightpulseai-net --body "2191216"
gh secret set PULSER_APP_PRIVATE_KEY --org Insightpulseai-net --body @pulser-hub.private-key.pem
```

**Phase 3: Workflow Updates**
For each repo, update `.github/workflows/projects-*.yml`:
- Replace `secrets.PROJECTS_TOKEN` with App token generation step
- Test workflow runs
- Verify project automation works

**Phase 4: PAT Retirement**
```bash
# Once all workflows use App tokens, delete PAT secrets
for repo in pulser-agent-framework pulser-mcp tbwa-fin-ops odoomation landing.io demo-repository; do
  gh secret delete PROJECTS_TOKEN --repo "Insightpulseai-net/$repo"
done

# Revoke PAT on GitHub settings
```

---

## 6. Verification Checklist

### A) Webhook Delivery Test

Check recent webhook deliveries on GitHub App settings page:
```
https://github.com/organizations/Insightpulseai-net/settings/installations/<installation_id>
→ Advanced → Recent Deliveries
```

Or via API:
```bash
gh api /app/hook/deliveries
```

### B) Installation Token Generation Test

From Node.js environment:
```javascript
import jwt from "jsonwebtoken";
import fs from "fs";

const appId = process.env.GITHUB_APP_ID;
const key = process.env.GITHUB_APP_PRIVATE_KEY;
const now = Math.floor(Date.now()/1000);

const token = jwt.sign(
  { iat: now-60, exp: now+600, iss: appId },
  key,
  { algorithm:"RS256" }
);

console.log("JWT:", token.slice(0,30)+"...");

// Then exchange JWT → installation token via GitHub API
```

### C) n8n Signature Validation Test

Trigger test event (e.g., create issue in test repo):
1. Check n8n execution log
2. Verify signature node passes
3. Confirm event routed correctly
4. Validate Supabase ops.run_events entry created

### D) Projects Automation Test

1. Create test issue with "learning" label
2. Verify workflow runs: `gh run list --repo Insightpulseai-net/pulser-mcp`
3. Check issue added to Learning Ops project
4. Confirm status set correctly

---

## 7. Troubleshooting

### Webhook 401/403 Errors

**Symptom**: GitHub returns 401/403 when delivering webhook

**Fix**:
- Regenerate webhook secret
- Update n8n credential
- Verify signature validation logic

### Installation Token 401

**Symptom**: API calls fail with "Bad credentials"

**Fix**:
- Verify App installed to org (not just owned)
- Check installation ID matches env var
- Regenerate private key if compromised

### Projects Automation Fails

**Symptom**: Workflow runs but items not added to project

**Fix**:
- Verify App has Projects: Read & write permission
- Check organization-level permission granted (not just repo)
- Confirm project ID/title matches template spec

---

## 8. Current vs. Target State

### Current State ❌
- PAT-based authentication (expires, user-scoped)
- Manual secret distribution across 6 repos
- No webhook signature validation
- No centralized event routing

### Target State ✅
- GitHub App installation tokens (org-scoped, auditable)
- Organization-level secrets (single source of truth)
- Secure webhook signature validation in n8n
- Centralized event routing with ops schema persistence
- Clean separation: n8n (webhooks) + mcp.insightpulseai.net (UI/API)

---

## 9. Next Steps

1. **Install pulser-hub app** to Insightpulseai-net organization
2. **Configure webhook** URL and secret on GitHub App settings
3. **Set organization secrets**: `PULSER_APP_ID`, `PULSER_APP_PRIVATE_KEY`
4. **Create n8n workflow** with signature validation + event routing
5. **Update workflows** in pulser-mcp to use App token
6. **Test end-to-end**: Create issue → Webhook → n8n → Supabase → Project automation
7. **Migrate remaining 5 repos** to use App token
8. **Retire PAT** and delete secrets

---

## References

- [GitHub Apps authentication](https://docs.github.com/apps/creating-github-apps/authenticating-with-a-github-app/about-authentication-with-a-github-app)
- [Creating installation access tokens](https://docs.github.com/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Webhook event payloads](https://docs.github.com/webhooks/webhook-events-and-payloads)
- [actions/create-github-app-token](https://github.com/actions/create-github-app-token)
