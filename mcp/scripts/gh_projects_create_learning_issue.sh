#!/usr/bin/env bash
set -euo pipefail

# Create a learning issue and add it to Learning Ops project
# Usage: ./gh_projects_create_learning_issue.sh <title> <link> <track>

TITLE="${1:?issue title required}"
LINK="${2:?learning link required}"
TRACK="${3:-Azure Fundamentals}"
REPO="${REPO:-Insightpulseai-net/pulser-agent-framework}"
ORG="${ORG:-Insightpulseai-net}"

need() { command -v "$1" >/dev/null 2>&1 || { echo "Missing dependency: $1"; exit 1; }; }
need gh; need jq

# Create issue
BODY=$(cat <<EOF
**Link**: $LINK
**Track**: $TRACK
**Outcome**: Notes

**Definition of Done:**
- [ ] 3 key concepts learned
- [ ] 1 rule-of-thumb identified
- [ ] 1 pitfall documented
- [ ] Artifact link added
EOF
)

ISSUE_URL=$(gh issue create --repo "$REPO" \
  --title "$TITLE" \
  --label learning \
  --body "$BODY" \
  --json url -q .url)

echo "Created issue: $ISSUE_URL"

# Add to Learning Ops project
./scripts/gh_projects_add_issue.sh "$ISSUE_URL" "TEMPLATE - Learning Ops" "Next"

echo "Added to Learning Ops project with status: Next"
