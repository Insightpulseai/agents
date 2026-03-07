#!/usr/bin/env bash
set -euo pipefail

# Stamp workspace configuration into a repository
# Usage: ./scripts/stamp_workspace.sh [repo-path] [workspace-name]

REPO_PATH="${1:-.}"
WORKSPACE_NAME="${2:-$(basename "$REPO_PATH")}"

TEMPLATE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../templates/workspace" && pwd)"

echo "=== Stamping workspace configuration ==="
echo "Repository: $REPO_PATH"
echo "Workspace name: $WORKSPACE_NAME"
echo "Template source: $TEMPLATE_DIR"
echo ""

cd "$REPO_PATH"

# Check if it's a git repo
if [[ ! -d .git ]]; then
  echo "❌ Error: Not a git repository"
  exit 1
fi

# Copy pyproject.toml
if [[ -f pyproject.toml ]]; then
  echo "⚠️  pyproject.toml exists - backing up to pyproject.toml.backup"
  cp pyproject.toml pyproject.toml.backup
fi
cp "$TEMPLATE_DIR/pyproject.toml" pyproject.toml
echo "✓ Copied pyproject.toml"

# Copy .vscode/settings.json
mkdir -p .vscode
if [[ -f .vscode/settings.json ]]; then
  echo "⚠️  .vscode/settings.json exists - backing up to .vscode/settings.json.backup"
  cp .vscode/settings.json .vscode/settings.json.backup
fi
cp "$TEMPLATE_DIR/settings.json" .vscode/settings.json
echo "✓ Copied .vscode/settings.json"

# Copy workspace file with custom name
WORKSPACE_FILE="${WORKSPACE_NAME}.code-workspace"
if [[ -f "$WORKSPACE_FILE" ]]; then
  echo "⚠️  $WORKSPACE_FILE exists - backing up to ${WORKSPACE_FILE}.backup"
  cp "$WORKSPACE_FILE" "${WORKSPACE_FILE}.backup"
fi
cp "$TEMPLATE_DIR/repo.code-workspace" "$WORKSPACE_FILE"
echo "✓ Copied $WORKSPACE_FILE"

echo ""
echo "=== Git status ==="
git status --short

echo ""
echo "=== Ready to commit? ==="
echo "Review the changes above, then run:"
echo ""
echo "  git add pyproject.toml .vscode/settings.json $WORKSPACE_FILE"
echo "  git commit -m \"chore(dev): add repo workspace + ruff config\""
echo "  git push"
echo ""
