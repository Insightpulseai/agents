#!/usr/bin/env bash
set -euo pipefail

SPEC="${1:?spec json required}"
ORG="${ORG:?set ORG=Insightpulseai-net}"

need() { command -v "$1" >/dev/null 2>&1 || { echo "Missing dependency: $1"; exit 1; }; }
need gh; need jq

TITLE="$(jq -r '.title' "$SPEC")"
FIELDS_JSON="$(jq -c '.fields' "$SPEC")"

ORG_ID="$(gh api graphql -f query='query($org:String!){organization(login:$org){id}}' -f org="$ORG" --jq '.data.organization.id')"

# Find existing project by title
PROJECT_ID="$(gh api graphql -f query='
query($org:String!,$first:Int!){
  organization(login:$org){
    projectsV2(first:$first){
      nodes{ id title number }
    }
  }
}' -f org="$ORG" -F first=100 --jq ".data.organization.projectsV2.nodes[] | select(.title==\"$TITLE\") | .id" | head -n1 || true)"

if [[ -z "${PROJECT_ID:-}" ]]; then
  echo "Creating project: $TITLE"
  PROJECT_ID="$(gh api graphql -f query='
mutation($ownerId:ID!,$title:String!){
  createProjectV2(input:{ownerId:$ownerId,title:$title}){ projectV2{ id number title } }
}' -f ownerId="$ORG_ID" -f title="$TITLE" --jq '.data.createProjectV2.projectV2.id')"
else
  echo "Project exists: $TITLE"
fi

echo "PROJECT_ID=$PROJECT_ID"

# Fetch existing fields
FIELDS_DUMP="$(gh api graphql -f query='
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
}' -f projectId="$PROJECT_ID")"

create_text_field() {
  local name="$1"
  gh api graphql -f query='
mutation($projectId:ID!,$name:String!){
  createProjectV2Field(input:{projectId:$projectId,name:$name,dataType:TEXT}){
    projectV2Field{ ... on ProjectV2FieldCommon { id name dataType } }
  }
}' -f projectId="$PROJECT_ID" -f name="$name" >/dev/null
}

create_number_field() {
  local name="$1"
  gh api graphql -f query='
mutation($projectId:ID!,$name:String!){
  createProjectV2Field(input:{projectId:$projectId,name:$name,dataType:NUMBER}){
    projectV2Field{ ... on ProjectV2FieldCommon { id name dataType } }
  }
}' -f projectId="$PROJECT_ID" -f name="$name" >/dev/null
}

create_date_field() {
  local name="$1"
  gh api graphql -f query='
mutation($projectId:ID!,$name:String!){
  createProjectV2Field(input:{projectId:$projectId,name:$name,dataType:DATE}){
    projectV2Field{ ... on ProjectV2FieldCommon { id name dataType } }
  }
}' -f projectId="$PROJECT_ID" -f name="$name" >/dev/null
}

create_single_select_field() {
  local name="$1"
  local options_json="$2"

  # Create the complete GraphQL payload as JSON
  local payload="$(jq -nc \
    --arg projectId "$PROJECT_ID" \
    --arg name "$name" \
    --argjson options "$options_json" \
    '{
      query: "mutation($projectId:ID!,$name:String!,$options:[ProjectV2SingleSelectFieldOptionInput!]!){createProjectV2Field(input:{projectId:$projectId,name:$name,dataType:SINGLE_SELECT,singleSelectOptions:$options}){projectV2Field{... on ProjectV2SingleSelectField{id name dataType}}}}",
      variables: {
        projectId: $projectId,
        name: $name,
        options: $options
      }
    }')"

  gh api graphql --input - <<<$''"$payload" >/dev/null
}

field_exists() {
  local name="$1"
  echo "$FIELDS_DUMP" | jq -e --arg n "$name" '.data.node.fields.nodes[]? | select(.name==$n) | .id' >/dev/null 2>&1
}

echo "$FIELDS_JSON" | jq -c '.[]' | while read -r f; do
  name="$(echo "$f" | jq -r '.name')"
  type="$(echo "$f" | jq -r '.type')"

  if field_exists "$name"; then
    echo "Field exists: $name"
    continue
  fi

  echo "Creating field: $name ($type)"
  case "$type" in
    text) create_text_field "$name" ;;
    number) create_number_field "$name" ;;
    date) create_date_field "$name" ;;
    single_select)
      opts="$(echo "$f" | jq -c '.options | map({name:., color:"GRAY", description:""})')"
      create_single_select_field "$name" "$opts"
      ;;
    *) echo "Unknown field type: $type"; exit 1 ;;
  esac
done

echo "Done. Re-fetch fields:"
gh api graphql -f query='
query($projectId:ID!){
  node(id:$projectId){
    ... on ProjectV2{
      title
      fields(first:100){
        nodes{
          __typename
          ... on ProjectV2FieldCommon { id name dataType }
          ... on ProjectV2SingleSelectField { id name dataType options { id name } }
        }
      }
    }
  }
}' -f projectId="$PROJECT_ID" --jq '.data.node.title, (.data.node.fields.nodes[] | {name, dataType, __typename})'
