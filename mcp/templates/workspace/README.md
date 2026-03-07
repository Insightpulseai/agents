# Org-Wide Workspace Configuration

Standard workspace configuration for all InsightPulse AI repositories.

## Files

- **pyproject.toml** - Ruff configuration (linting, formatting, import sorting)
- **settings.json** - VSCode settings (format on save, search excludes, Ruff integration)
- **repo.code-workspace** - Multi-root workspace configuration

## Quick Setup

### Option 1: Use the stamp script (recommended)

```bash
# From any repo
/path/to/pulser-mcp/scripts/stamp_workspace.sh

# Or from pulser-mcp
cd /path/to/target-repo
/path/to/pulser-mcp/scripts/stamp_workspace.sh . my-repo-name
```

### Option 2: Manual copy

```bash
cd /path/to/target-repo

# Copy templates
cp /path/to/pulser-mcp/templates/workspace/pyproject.toml .
mkdir -p .vscode
cp /path/to/pulser-mcp/templates/workspace/settings.json .vscode/
cp /path/to/pulser-mcp/templates/workspace/repo.code-workspace my-repo.code-workspace

# Commit
git add pyproject.toml .vscode/settings.json my-repo.code-workspace
git commit -m "chore(dev): add repo workspace + ruff config"
git push
```

## What This Fixes

### Ruff Issues
- ✅ "No pyproject.toml found" errors
- ✅ Slow indexing of vendor/core code
- ✅ False positives on Odoo/OCA patterns

### VSCode Issues
- ✅ Slow file watching (ignores vendor directories)
- ✅ Slow search (excludes irrelevant directories)
- ✅ Python analysis slowness (excludes vendor code)
- ✅ Format on save enabled by default

### Developer Experience
- ✅ Consistent configuration across all repos
- ✅ Faster IDE performance
- ✅ Automatic code formatting
- ✅ Import organization on save

## Customization

If a repo needs custom Ruff rules:

1. Copy the template as-is
2. Add repo-specific rules to the existing sections
3. Keep the exclude patterns (critical for performance)

Example:
```toml
[tool.ruff.lint]
select = ["E", "F", "I"]
ignore = ["E501"]

# Add repo-specific rules
extend-select = ["B", "C4"]  # Add bugbear and comprehensions
```

## Testing

After applying the template:

1. Reload VSCode window
2. Open a Python file
3. Verify Ruff is working (should see linting in the editor)
4. Make a formatting change and save (should auto-format)
5. Search for a term (should be fast, ignoring vendor directories)

## Troubleshooting

**Ruff not working?**
- Check `.vscode/settings.json` has `ruff.enable: true`
- Verify `pyproject.toml` exists in repo root
- Reload VSCode window

**VSCode still slow?**
- Check `.vscode/settings.json` has correct excludes
- Run "Developer: Show Running Extensions" and disable unused ones
- Consider excluding additional directories in search.exclude

**Format on save not working?**
- Check `.vscode/settings.json` has `editor.formatOnSave: true`
- Verify Ruff extension is installed and enabled
- Check file is not excluded by Ruff config
