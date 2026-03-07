#!/usr/bin/env bash
set -euo pipefail

# Add an issue/PR to a project and set its status
# Usage: ./gh_projects_add_issue.sh <project-title> <resource-url> <status>

PROJECT_TITLE="${1:?project title required}"
RESOURCE_URL="${2:?issue/pr url required}"
STATUS_NAME="${3:-Next}"

ORG="${ORG:?set ORG=Insightpulseai-net}"
: "${GH_TOKEN:?set GH_TOKEN (PAT with project, read:org, repo)}"

need() { command -v "$1" >/dev/null 2>&1 || { echo "Missing dependency: $1"; exit 1; }; }
need gh; need jq

# Find project id by title
PROJECT_ID="$(gh api graphql -f query='
query($org:String!,$first:Int!){
  organization(login:$org){
    projectsV2(first:$first){ nodes{ id title } }
  }
}' -f org="$ORG" -F first=100 --jq ".data.organization.projectsV2.nodes[] | select(.title==\"$PROJECT_TITLE\") | .id" | head -n1)"

[[ -n "$PROJECT_ID" ]] || { echo "Project not found: $PROJECT_TITLE"; exit 1; }

# Resolve resource (Issue or PullRequest) to node id
CONTENT_ID="$(gh api graphql -f query='
query($url:URI!){
  resource(url:$url){
    __typename
    ... on Issue { id }
    ... on PullRequest { id }
  }
}' -f url="$RESOURCE_URL" --jq '.data.resource.id')"

[[ -n "$CONTENT_ID" ]] || { echo "Could not resolve resource id for: $RESOURCE_URL"; exit 1; }

# Add item (skip if already exists)
ITEM_ID="$(gh api graphql -f query='
mutation($projectId:ID!,$contentId:ID!){
  addProjectV2ItemById(input:{projectId:$projectId,contentId:$contentId}){
    item{ id }
  }
}' -f projectId="$PROJECT_ID" -f contentId="$CONTENT_ID" --jq '.data.addProjectV2ItemById.item.id' 2>/dev/null || true)"

if [[ -z "$ITEM_ID" ]]; then
  echo "Item already in project or add failed: $RESOURCE_URL"
  exit 0
fi

echo "Added to project. Item ID: $ITEM_ID"

# Get Status field + option ids
FIELDS="$(gh api graphql -f query='
query($projectId:ID!){
  node(id:$projectId){
    ... on ProjectV2{
      fields(first:100){
        nodes{
          ... on ProjectV2SingleSelectField { id name options{ id name } }
        }
      }
    }
  }
}' -f projectId="$PROJECT_ID")"

STATUS_FIELD_ID="$(echo "$FIELDS" | jq -r '.data.node.fields.nodes[] | select(.name=="Status") | .id' | head -n1)"
STATUS_OPT_ID="$(echo "$FIELDS" | jq -r --arg s "$STATUS_NAME" '.data.node.fields.nodes[] | select(.name=="Status") | .options[] | select(.name==$s) | .id' | head -n1)"

if [[ -n "${STATUS_FIELD_ID:-}" && -n "${STATUS_OPT_ID:-}" ]]; then
  gh api graphql -f query='
mutation($projectId:ID!,$itemId:ID!,$fieldId:ID!,$optionId:String!){
  updateProjectV2ItemFieldValue(input:{
    projectId:$projectId,itemId:$itemId,fieldId:$fieldId,
    value:{singleSelectOptionId:$optionId}
  }){ clientMutationId }
}' -f projectId="$PROJECT_ID" -f itemId="$ITEM_ID" -f fieldId="$STATUS_FIELD_ID" -f optionId="$STATUS_OPT_ID" >/dev/null
  echo "Added to project + set Status=$STATUS_NAME: $RESOURCE_URL"
else
  echo "Added to project (Status not set; field/option missing): $RESOURCE_URL"
fi
