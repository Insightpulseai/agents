# GitHub Projects - Secrets Setup

## Required Secrets

The GitHub Actions workflows require a Personal Access Token (PAT) with appropriate permissions.

### Creating the PAT

1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Name: `GitHub Projects Automation`
4. Expiration: Choose appropriate duration (recommend 90 days with renewal reminder)
5. Select scopes:
   - ✅ `repo` (Full control of private repositories)
   - ✅ `read:org` (Read org and team membership)
   - ✅ `project` (Full control of projects)
6. Click "Generate token"
7. **Copy the token immediately** (you won't see it again)

### Setting Repository Secret

```bash
# Set secret for specific repository
gh secret set PROJECTS_TOKEN -R Insightpulseai-net/pulser-agent-framework
# Paste token when prompted

# Verify secret is set
gh secret list -R Insightpulseai-net/pulser-agent-framework
```

### Setting Organization Secret (Recommended)

If you have admin access to the organization, setting an org-level secret allows all repositories to use the same token:

```bash
# Set org-level secret
gh secret set PROJECTS_TOKEN --org Insightpulseai-net
# Paste token when prompted

# Configure repository access (choose one):
# 1. All repositories
gh secret set PROJECTS_TOKEN --org Insightpulseai-net --visibility all

# 2. Selected repositories only
gh secret set PROJECTS_TOKEN --org Insightpulseai-net --visibility selected \
  --repos "pulser-agent-framework,pulser-mcp,odoomation"

# 3. Private repositories only
gh secret set PROJECTS_TOKEN --org Insightpulseai-net --visibility private

# Verify org secret
gh secret list --org Insightpulseai-net
```

### Manual Setup via GitHub UI

**Repository Secret:**
1. Go to repository → Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Name: `PROJECTS_TOKEN`
4. Value: [paste PAT]
5. Click "Add secret"

**Organization Secret:**
1. Go to organization Settings → Secrets and variables → Actions
2. Click "New organization secret"
3. Name: `PROJECTS_TOKEN`
4. Value: [paste PAT]
5. Repository access: Choose visibility level
6. Click "Add secret"

## Token Security Best Practices

### Rotation Schedule
- **Development tokens**: Rotate every 30 days
- **Production tokens**: Rotate every 90 days
- Set calendar reminders 7 days before expiration

### Monitoring
```bash
# Check when token was last used (via workflow runs)
gh run list --workflow=projects-autoadd-learning.yml --limit 1

# Audit organization token usage
gh api /orgs/Insightpulseai-net/audit-log \
  --jq '.[] | select(.action=="token.create" or .action=="token.delete")'
```

### Emergency Revocation
```bash
# If token is compromised:
# 1. Revoke immediately via GitHub UI (Settings → Developer settings → PAT)
# 2. Generate new token
# 3. Update secret
gh secret set PROJECTS_TOKEN -R Insightpulseai-net/pulser-agent-framework

# 4. Verify workflows still work
gh workflow run projects-weekly-verify.yml
```

## Verification

### Test Workflows
```bash
# Trigger manual verification
gh workflow run projects-weekly-verify.yml --repo Insightpulseai-net/pulser-agent-framework

# Watch workflow run
gh run watch

# Check recent runs
gh run list --workflow=projects-weekly-verify.yml --limit 5
```

### Test Auto-add (Learning)
```bash
# Create test issue with learning label
gh issue create --repo Insightpulseai-net/pulser-agent-framework \
  --title "Test: Learning Ops Auto-add" \
  --label learning \
  --body "Testing automated project addition"

# Should trigger projects-autoadd-learning.yml
# Check workflow run
gh run list --workflow=projects-autoadd-learning.yml --limit 1
```

### Test Auto-add (Delivery)
```bash
# Create test PR with feature label
git checkout -b feature/test-auto-add
echo "test" > test.txt
git add test.txt
git commit -m "test: auto-add to delivery ops"
git push origin feature/test-auto-add

gh pr create --title "Test: Delivery Ops Auto-add" \
  --label feature \
  --body "Testing automated PR project addition"

# Should trigger projects-autoadd-delivery.yml
# Check workflow run
gh run list --workflow=projects-autoadd-delivery.yml --limit 1
```

## Troubleshooting

### Error: "Resource not accessible by integration"
**Cause**: Token lacks required scopes
**Fix**: Regenerate token with `project`, `read:org`, `repo` scopes

### Error: "Project not found"
**Cause**: Project title mismatch or token lacks org access
**Fix**:
```bash
# Verify project exists
export ORG="Insightpulseai-net"
export GH_TOKEN="<your-pat>"
gh api graphql -f query='
query($org:String!){
  organization(login:$org){
    projectsV2(first:10){ nodes{ title } }
  }
}' -f org="$ORG"
```

### Error: "Secret not found"
**Cause**: Secret not set or wrong name
**Fix**:
```bash
# List secrets
gh secret list -R Insightpulseai-net/pulser-agent-framework

# Should show: PROJECTS_TOKEN
```

### Workflow Not Triggering
**Cause**: Workflow file syntax error or permissions issue
**Fix**:
```bash
# Validate workflow syntax
gh workflow view projects-autoadd-learning.yml

# Check workflow status
gh workflow list

# Re-enable if disabled
gh workflow enable projects-autoadd-learning.yml
```

## Security Checklist

- [ ] PAT has minimal required scopes (`project`, `read:org`, `repo`)
- [ ] PAT expiration set (max 90 days)
- [ ] Secret stored in GitHub Secrets (not in code)
- [ ] Org-level secret preferred over repo-level (if admin access)
- [ ] Calendar reminder set for token rotation
- [ ] Test workflows verified after setup
- [ ] Emergency revocation procedure documented
- [ ] Token usage audited monthly

## References

- [GitHub PAT Documentation](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)
- [GitHub Secrets Documentation](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [GitHub Projects API](https://docs.github.com/en/graphql/reference/objects#projectv2)
