#!/bin/bash
# Pre-commit secret scan
# Checks staged files for common secret patterns

PATTERNS=(
  'AKIA[0-9A-Z]{16}'           # AWS Access Key
  'sk-[a-zA-Z0-9]{48}'         # OpenAI/Anthropic API Key
  'ghp_[a-zA-Z0-9]{36}'        # GitHub Personal Access Token
  'password\s*=\s*["\x27][^"\x27]+'  # Hardcoded passwords
)

STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACM 2>/dev/null)

if [ -z "$STAGED_FILES" ]; then
  exit 0
fi

FOUND=0
for pattern in "${PATTERNS[@]}"; do
  MATCHES=$(echo "$STAGED_FILES" | xargs grep -lE "$pattern" 2>/dev/null)
  if [ -n "$MATCHES" ]; then
    echo "WARNING: Potential secret found matching pattern '$pattern' in:" >&2
    echo "$MATCHES" >&2
    FOUND=1
  fi
done

if [ "$FOUND" -eq 1 ]; then
  echo "Secret scan found potential issues. Review before committing." >&2
  exit 1
fi

exit 0
