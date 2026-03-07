#!/usr/bin/env bash
set -euo pipefail

ORG="${ORG:?set ORG=Insightpulseai-net}"
TITLE="${1:?project title required}"

PROJECT="$(gh api graphql -f query='
query($org:String!,$first:Int!){
  organization(login:$org){
    projectsV2(first:$first){ nodes{ id title number } }
  }
}' -f org="$ORG" -F first=100)"

PROJECT_ID="$(echo "$PROJECT" | jq -r ".data.organization.projectsV2.nodes[] | select(.title==\"$TITLE\") | .id" | head -n1)"
[[ -n "$PROJECT_ID" ]] || { echo "Project not found: $TITLE"; exit 1; }

echo "PROJECT_ID=$PROJECT_ID"

gh api graphql -f query='
query($projectId:ID!){
  node(id:$projectId){
    ... on ProjectV2{
      title number
      fields(first:100){
        nodes{
          __typename
          ... on ProjectV2FieldCommon { id name dataType }
          ... on ProjectV2SingleSelectField { id name dataType options { id name } }
        }
      }
    }
  }
}' -f projectId="$PROJECT_ID" --jq '.data.node'
