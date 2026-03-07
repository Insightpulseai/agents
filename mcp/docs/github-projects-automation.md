# GitHub Projects Automation

Programmatic setup and management of GitHub Projects for Insightpulseai-net organization.

## Setup

### Prerequisites

```bash
# Install dependencies
brew install gh jq

# Authenticate with GitHub
gh auth login
gh auth refresh -h github.com -s project,read:org,repo,write:org
```

### Environment

```bash
export ORG="Insightpulseai-net"
export REPO="Insightpulseai-net/pulser-agent-framework"
```

## Usage

### Create Projects from Templates

```bash
# Create Learning Ops project
./scripts/gh_projects_apply.sh spec/projects/learning_ops.json

# Create Delivery Ops project
./scripts/gh_projects_apply.sh spec/projects/delivery_ops.json
```

### Verify Projects

```bash
# Verify Learning Ops
./scripts/gh_projects_verify.sh "TEMPLATE - Learning Ops"

# Verify Delivery Ops
./scripts/gh_projects_verify.sh "TEMPLATE - Delivery Ops"
```

### Create and Add Issues

#### Create Learning Issue (Automated)

```bash
# Create learning issue and add to project
./scripts/gh_projects_create_learning_issue.sh \
  "Learn: Introduction to Azure Well-Architected Framework" \
  "https://learn.microsoft.com/azure/well-architected/" \
  "Azure Fundamentals"
```

#### Add Existing Issue to Project

```bash
# Add issue by URL
./scripts/gh_projects_add_issue.sh \
  "https://github.com/Insightpulseai-net/pulser-agent-framework/issues/123" \
  "TEMPLATE - Learning Ops" \
  "In Progress"
```

#### Manual Issue Creation

```bash
# Create issue manually
ISSUE_URL=$(gh issue create --repo "$REPO" \
  --title "Learn: Azure Security Best Practices" \
  --label learning \
  --body "Link: https://learn.microsoft.com/azure/security/..." \
  --json url -q .url)

# Add to project
./scripts/gh_projects_add_issue.sh "$ISSUE_URL" "TEMPLATE - Learning Ops" "Next"
```

## Project Templates

### Learning Ops

**Fields:**
- **Status**: Backlog, Next, In Progress, Blocked, Done, Archived
- **Track**: Azure Fundamentals, AI/Agents, Power BI, Security, Odoo, Supabase, DevOps
- **Type**: Module, Lab, Reading, Build, Writeup, Exam
- **Outcome**: Notes, Demo, PR, Checklist, Blog
- **Effort (min)**: Number field
- **Difficulty**: 1-5 scale
- **Link**: URL to learning resource
- **Artifact**: URL to deliverable
- **Due**: Date field

**Workflow:**
1. Create issue with `learning` label
2. Auto-add to Learning Ops project
3. Set status to "Next"
4. Track progress through Status field
5. Add artifact link when complete

### Delivery Ops

**Fields:**
- **Status**: Backlog, Ready, In Progress, Review, Blocked, Done
- **Repo**: pulser-agent-framework, pulser-mcp, odoomation, landing.io, demo-repository
- **Type**: Feature, Bug, Chore, Security, Infra, Docs
- **Priority**: P0, P1, P2, P3
- **Effort**: S, M, L, XL
- **Release**: Text field for version
- **Due**: Date field
- **Artifact**: URL to PR or deployment

**Workflow:**
1. Create issue with relevant labels
2. Add to Delivery Ops project
3. Set repo, type, priority, effort
4. Track through Status field
5. Link PR or deployment URL

## Advanced Usage

### Query Projects

```bash
# List all organization projects
gh api graphql -f query='
query($org:String!){
  organization(login:$org){
    projectsV2(first:100){
      nodes{ id title number }
    }
  }
}' -f org="$ORG" --jq '.data.organization.projectsV2.nodes[]'

# Get project fields
PROJECT_ID="..." # from above
gh api graphql -f query='
query($projectId:ID!){
  node(id:$projectId){
    ... on ProjectV2{
      fields(first:100){
        nodes{
          __typename
          ... on ProjectV2FieldCommon { id name dataType }
          ... on ProjectV2SingleSelectField { id name dataType options { id name } }
        }
      }
    }
  }
}' -f projectId="$PROJECT_ID" --jq '.data.node.fields.nodes[]'
```

### Update Field Values

```bash
# Update text field
gh api graphql -f query='
mutation($projectId:ID!,$itemId:ID!,$fieldId:ID!,$value:String!){
  updateProjectV2ItemFieldValue(input:{
    projectId:$projectId,itemId:$itemId,fieldId:$fieldId,
    value:{text:$value}
  }){ clientMutationId }
}' -f projectId="$PROJECT_ID" -f itemId="$ITEM_ID" -f fieldId="$FIELD_ID" -f value="$VALUE"

# Update number field
gh api graphql -f query='
mutation($projectId:ID!,$itemId:ID!,$fieldId:ID!,$value:Float!){
  updateProjectV2ItemFieldValue(input:{
    projectId:$projectId,itemId:$itemId,fieldId:$fieldId,
    value:{number:$value}
  }){ clientMutationId }
}' -f projectId="$PROJECT_ID" -f itemId="$ITEM_ID" -f fieldId="$FIELD_ID" -F value="$VALUE"

# Update date field
gh api graphql -f query='
mutation($projectId:ID!,$itemId:ID!,$fieldId:ID!,$value:Date!){
  updateProjectV2ItemFieldValue(input:{
    projectId:$projectId,itemId:$itemId,fieldId:$fieldId,
    value:{date:$value}
  }){ clientMutationId }
}' -f projectId="$PROJECT_ID" -f itemId="$ITEM_ID" -f fieldId="$FIELD_ID" -f value="$VALUE"
```

## Automated Workflows

### Setup Required Secret

**CRITICAL**: Workflows require a Personal Access Token with `project`, `read:org`, `repo` scopes.

See [GitHub Projects Secrets Setup](github-projects-secrets.md) for detailed instructions.

```bash
# Quick setup (repository-level)
gh secret set PROJECTS_TOKEN -R Insightpulseai-net/pulser-agent-framework
# Paste PAT when prompted

# Recommended: Org-level secret (if admin access)
gh secret set PROJECTS_TOKEN --org Insightpulseai-net --visibility all
```

### Active Workflows

#### 1. Auto-add Learning Issues
**File**: [.github/workflows/projects-autoadd-learning.yml](../.github/workflows/projects-autoadd-learning.yml)

**Trigger**: Issue labeled with `learning`
**Action**: Add to "TEMPLATE - Learning Ops" with status "Next"

**Test**:
```bash
gh issue create --repo Insightpulseai-net/pulser-agent-framework \
  --title "Learn: Azure Fundamentals" \
  --label learning \
  --body "Link: https://learn.microsoft.com/azure/"
```

#### 2. Auto-add Delivery PRs
**File**: [.github/workflows/projects-autoadd-delivery.yml](../.github/workflows/projects-autoadd-delivery.yml)

**Trigger**: PR labeled with `feature`, `bug`, `infra`, `security`, `docs`, or `chore`
**Action**: Add to "TEMPLATE - Delivery Ops" with status "Review"

**Test**:
```bash
git checkout -b feature/test-workflow
echo "test" > test.txt
git add test.txt && git commit -m "test: workflow"
git push origin feature/test-workflow
gh pr create --title "Test PR" --label feature --body "Testing auto-add"
```

#### 3. Weekly Project Verification
**File**: [.github/workflows/projects-weekly-verify.yml](../.github/workflows/projects-weekly-verify.yml)

**Trigger**: Every Monday at 00:00 UTC (cron: `0 0 * * 1`)
**Action**: Verify both project templates have correct fields

**Manual Trigger**:
```bash
gh workflow run projects-weekly-verify.yml
gh run watch  # Watch live
```

#### 4. Auto-labeling
**File**: [.github/workflows/projects-auto-label.yml](../.github/workflows/projects-auto-label.yml)

**Trigger**: Issue/PR opened or edited

**Auto-label Rules**:

**Issues:**
- Contains `learn.microsoft.com` or starts with `Learn:` → `learning`
- Contains `azure` → `azure`
- Contains `power bi` → `power-bi`
- Contains `odoo` → `odoo`
- Contains `supabase` → `supabase`
- Contains `ai` or `agent` → `ai`

**PRs:**
- Branch `feature/*` → `feature`
- Branch `fix/*` or `bugfix/*` → `bug`
- Branch `infra/*` → `infra`
- Branch `security/*` → `security`
- Branch `docs/*` → `docs`
- Branch `chore/*` → `chore`
- Title contains `[P0]` or `critical` → `P0`
- Title contains `[P1]` or `urgent` → `P1`

**Example**:
```bash
# This issue gets auto-labeled with 'learning' and 'azure'
gh issue create \
  --title "Learn: Azure Well-Architected Framework" \
  --body "Link: https://learn.microsoft.com/azure/well-architected/"

# Then auto-added to Learning Ops by projects-autoadd-learning workflow
```

## References

- [GitHub Projects GraphQL API](https://docs.github.com/en/graphql/reference/objects#projectv2)
- [GitHub CLI](https://cli.github.com/manual/)
- [Project Templates Spec](spec/projects/)
