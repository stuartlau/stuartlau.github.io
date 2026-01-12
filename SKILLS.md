# Development Skills & Tools

This document lists all development tools, skills, and commands available for this project.

## 🧪 Testing

| Tool | Command | Purpose |
|------|---------|---------|
| **pytest** | `npm run test` | Run Python tests |
| **pytest-cov** | `npm run test:coverage` | Generate coverage report |

```bash
# Run tests
pytest scripts/

# With coverage
pytest --cov=scripts --cov-report=html
```

---

## 🎨 Code Quality & Formatting

### Python
| Tool | Command | Purpose |
|------|---------|---------|
| **black** | `npm run format:python` | Code formatter |
| **isort** | `npm run format:python` | Import sorter |
| **flake8** | `npm run lint:python` | Linter |
| **mypy** | `npm run lint:python:strict` | Type checker |

### JavaScript
| Tool | Command | Purpose |
|------|---------|---------|
| **ESLint** | `npx eslint .` | JS/TS linting |
| **terser** | `npm run minify:js` | JS minification |
| **clean-css** | `npm run minify:css` | CSS minification |

### Markdown
| Tool | Command | Purpose |
|------|---------|---------|
| **markdownlint** | `npm run markdown:lint` | Lint markdown |
| **remark** | `npm run markdown:fix` | Format markdown |

---

## 🔒 Security & Audit

| Tool | Command | Purpose |
|------|---------|---------|
| **gitleaks** | `npm run gitleaks` | Detect secrets/credentials |
| **pip-audit** | `npm run audit:python` | Scan Python dependencies |
| **npm audit** | `npm run audit:npm` | Scan npm dependencies |
| **trufflehog** | `trufflehog filesystem .` | Deep secret scanning |

```bash
# Full security audit
npm run audit

# Check for leaked secrets
gitleaks detect --source=. --verbose
```

---

## 📊 Performance & Lighthouse

| Tool | Command | Purpose |
|------|---------|---------|
| **Lighthouse CI** | `npm run lighthouse` | Performance audits |
| **imagemin** | `npm run build:images` | Image compression |
| **svgo** | `npm run build:svg` | SVG optimization |

```bash
# Run Lighthouse CI
lhci autorun --config=.lighthouserc.json

# Optimize all images
imagemin images/**/* --out-dir=images-optimized
```

---

## 🔧 Development Workflow

### Commit Messages
| Tool | Command | Purpose |
|------|---------|---------|
| **commitizen** | `npm run commit` | Interactive commit wizard |
| **commitlint** | Automatic via hook | Validate commit format |

```bash
# Interactive commit (recommended)
npm run commit

# Conventional commit types:
# feat, fix, docs, style, refactor, perf, test, chore, security, delete
```

### Git Hooks
| Hook | Trigger | Purpose |
|------|---------|---------|
| **pre-commit** | Before commit | Code quality checks |
| **commit-msg** | After message | Validate format |
| **post-commit** | After commit | Show summary |
| **post-push** | After push | Show stats |

```bash
# Install hooks
npm run install:hooks

# Skip hooks (not recommended)
git commit --no-verify -m "message"
```

---

## 🧹 Cleanup Commands

| Command | Purpose |
|---------|---------|
| `npm run clean` | Remove cache/build files |
| `npm run clean:all` | Remove everything (including node_modules) |
| `rimraf node_modules` | Force remove node_modules |

---

## 🔍 Search & Find

| Tool | Command | Purpose |
|------|---------|---------|
| **ripgrep** | `npm run ripgrep` | Search for TODO/FIXME/BUG |
| **fd** | `fd -e py -e md` | Fast file finder |
| **rg** | `rg "pattern"` | Content search |

```bash
# Search for TODO/FIXME comments
rg -i 'TODO|FIXME|BUG|HACK' --type py --type js --type md

# Find all Python files
fd -e py

# Search in files
rg "import requests" --type py
```

---

## 📦 Package Management

### Python
```bash
# Install dependencies
pip3 install -r requirements.txt

# Audit dependencies
pip-audit

# Format code
black scripts/ && isort scripts/

# Lint
flake8 scripts/ --max-line-length=100
mypy scripts/
```

### Node.js
```bash
# Install dependencies
npm install

# Audit
npm audit
npm audit fix

# Update packages
npm update
```

---

## 🚀 Deployment Scripts

```bash
# Build Jekyll site
jekyll build

# Build with optimizations
npm run build:assets
npm run minify:js
npm run minify:css

# Run Lighthouse CI
npm run lighthouse
```

---

## 📋 Quick Reference

| Task | Command |
|------|---------|
| Run tests | `npm run test` |
| Format code | `npm run format:python` |
| Lint code | `npm run lint:python` |
| Security audit | `npm run audit` |
| Optimize images | `npm run build:images` |
| Minify assets | `npm run build:assets` |
| Make commit | `npm run commit` |
| Check secrets | `gitleaks detect` |
| Clean cache | `npm run clean` |

---

## 🛠 Installed Tools Summary

### Python Tools
- `pytest` - Testing framework
- `pytest-cov` - Coverage reporting
- `black` - Code formatter
- `isort` - Import sorter
- `flake8` - Linter
- `mypy` - Type checker
- `pip-audit` - Dependency auditor
- `cookiecutter` - Project templates
- `copier` - Project templates

### Node.js Tools
- `pre-commit` - Git hooks framework
- `@commitlint/cli` - Commit message validation
- `commitizen` - Interactive commits
- `imagemin` - Image optimization
- `terser` - JS minification
- `clean-css-cli` - CSS minification
- `lighthouse` - Performance auditing
- `@lhci/cli` - Lighthouse CI
- `markdownlint-cli` - Markdown linting
- `remark-cli` - Markdown processing
- `svgo` - SVG optimization
- `eslint` - JavaScript linting
- `rimraf` - Safe deletion
- `npm-run-all` - Script orchestration

### CLI Tools (via Homebrew)
- `gitleaks` - Secret detection
- `fd` - Fast file finder
- `ripgrep` - Powerful grep
- `fselect` - SQL-like file queries
- `jq` - JSON processor
- `yq` - YAML processor

---

## 📖 Resources

- [Pre-commit Docs](https://pre-commit.com/)
- [Commitlint](https://commitlint.js.org/)
- [Lighthouse CI](https://github.com/GoogleChrome/lighthouse-ci)
- [pytest Docs](https://docs.pytest.org/)
- [Black Docs](https://black.readthedocs.io/)
- [Gitleaks](https://github.com/gitleaks/gitleaks)
