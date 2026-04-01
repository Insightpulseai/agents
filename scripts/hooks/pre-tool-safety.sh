#!/bin/bash
# Pre-tool safety check for Bash commands
# Blocks dangerous operations like rm -rf /, force pushes to main, etc.

COMMAND="${CLAUDE_TOOL_INPUT:-}"

# Block force push to main/master
if echo "$COMMAND" | grep -qE 'git\s+push\s+.*--force.*\s+(main|master)'; then
  echo "BLOCKED: Force push to main/master is not allowed" >&2
  exit 1
fi

# Block rm -rf on root or home
if echo "$COMMAND" | grep -qE 'rm\s+-rf\s+(/|~/|\$HOME)'; then
  echo "BLOCKED: Dangerous rm -rf target" >&2
  exit 1
fi

exit 0
