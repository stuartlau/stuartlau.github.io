# Git Hooks Configuration

This repository uses Git hooks to enforce code quality and standardize commit messages.

## Installed Hooks

### Pre-Commit Hook (`.git/hooks/pre-commit`)
Automatically runs code quality checks before each commit:
- **trailing-whitespace**: Removes trailing whitespace
- **end-of-file-fixer**: Ensures files end with newline
- **check-yaml**: Validates YAML syntax
- **check-json**: Validates JSON syntax
- **check-added-large-files**: Prevents large file commits (>1MB)
- **detect-private-key**: Detects private key files
- **isort**: Sorts Python imports
- **black**: Formats Python code
- **shellcheck**: Checks shell script quality

### Commit Message Hook (`.git/hooks/commit-msg`)
Validates commit message format using [commitlint](https://commitlint.js.org/):

```
<type>(<scope>): <subject>

Allowed types:
- feat: New feature
- fix: Bug fix
- docs: Documentation changes
- style: Formatting, missing semicolons, etc.
- refactor: Code refactoring
- perf: Performance improvements
- test: Adding tests
- chore: Maintenance tasks
- security: Security fixes
- delete: Deleting files
```

Example commit messages:
```
feat: Add user authentication module
fix: resolve memory leak in cache
docs: update API documentation
security: patch vulnerability in dependencies
```

### Post-Commit Hook (`.git/hooks/post-commit`)
Displays commit summary after successful commit:
- Commit hash
- Branch name
- Commit message
- Lines added/removed
- Files changed

### Post-Push Hook (`.git/hooks/post-push`)
Displays push summary after pushing:
- Branch pushed
- Remote name
- Number of commits
- Repository URL
- Link to GitHub Actions

## Installation

### Pre-commit Framework
```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install

# Update hooks to latest versions
pre-commit autoupdate
```

### Commitlint
```bash
# Global installation
npm install -g @commitlint/cli @commitlint/config-conventional

# Or use via npx
npx @commitlint/cli --config .commitlintrc.js
```

## Configuration Files

| File | Purpose |
|------|---------|
| `.pre-commit-config.yaml` | Pre-commit hook configuration |
| `.commitlintrc.js` | Commit message validation rules |

## Running Hooks Manually

```bash
# Run all pre-commit hooks
pre-commit run --all-files

# Run specific hook
pre-commit run trailing-whitespace

# Skip pre-commit hooks (use with caution)
git commit --no-verify -m "message"
```

## Troubleshooting

### Hooks not running?
```bash
# Verify hooks are installed
cat .git/hooks/pre-commit | head -5
```

### Pre-commit errors
```bash
# Check pre-commit log
cat ~/.cache/pre-commit/pre-commit.log
```

### Update hook versions
```bash
pre-commit autoupdate
pre-commit install
```
