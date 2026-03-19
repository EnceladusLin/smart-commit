# 🧠 SmartCommit

> AI-powered git commit message generator that writes your commit messages for you.

[![CI](https://github.com/EnceladusLin/smart-commit/actions/workflows/ci.yml/badge.svg)](https://github.com/EnceladusLin/smart-commit/actions/workflows/ci.yml)
[![License](https://img.shields.io/github/license/EnceladusLin/smart-commit)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](#requirements)

**SmartCommit** analyzes your staged git changes and generates meaningful, conventional commit messages using AI. No more staring at a blank terminal wondering how to summarize your changes.

## Why this exists

Writing good commit messages is annoying, repetitive, and easy to postpone. SmartCommit turns:

- `git add .`
- `uh... what do I call this commit?`

into:

- `smart-commit`
- review suggestion
- hit confirm

It is built for real developer workflows, not toy demos.

## ✨ Features

- 🚀 **One-command** commit message generation
- 📝 **Conventional Commits** format by default
- 🤖 **Multiple AI providers**: OpenAI, Anthropic Claude, Ollama (local)
- ⚡ **Fast**: Only analyzes staged changes, not entire repo
- 🔒 **Privacy-first**: Your code never leaves your machine in local mode
- 🎨 **Customizable**: Configure style, format, and behavior
- 📦 **Works offline** with local AI via Ollama
- ✅ **Interactive approval flow** before commit

## Demo

```bash
git add .
smart-commit
```

Example output:

```text
Analyzing staged changes...
  src/auth.py (+45 -12)
  tests/test_auth.py (+28 -5)
  README.md (+3 -1)

Using anthropic / claude-sonnet-4-6
⠋ Generating commit message...

Suggested commit message:
feat(auth): add JWT token refresh mechanism
- implement refresh_token endpoint
- add expiration check before validation
- update tests for new refresh flow
- fix README auth example
```

## 📋 Requirements

- Python 3.8+
- Git
- At least one AI provider configured

## 🛠️ Installation

```bash
pip install git+https://github.com/EnceladusLin/smart-commit.git
```

For local development:

```bash
git clone https://github.com/EnceladusLin/smart-commit.git
cd smart-commit
pip install -e .[dev]
```

## 🔧 Configuration

### OpenAI

```bash
export OPENAI_API_KEY="sk-..."
```

### Anthropic Claude

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

### Ollama (local / free)

```bash
ollama pull codellama
export OLLAMA_HOST="http://localhost:11434"
```

## 🎯 Usage

```bash
# stage your changes first
git add .

# generate a commit message
smart-commit

# short alias
sc
```

### Advanced usage

```bash
smart-commit --provider openai
smart-commit --provider anthropic
smart-commit --provider ollama
smart-commit --style conventional
smart-commit --style short
smart-commit --dry-run
smart-commit --edit
smart-commit --auto-stage
```

## 📖 Example config

Location: `~/.smart-commit/config.yaml`

```yaml
ai:
  provider: openai
  model: gpt-4o-mini
  temperature: 0.7

commit:
  style: conventional
  max_length: 72
  include_scope: true

git:
  auto_stage: false
  auto_push: false
```

## 🧪 Development

```bash
pip install -e .[dev]
pytest
ruff check src tests
mypy src
```

## Growth angle

SmartCommit is designed to be:
- easy to screenshot
- easy to demo in a terminal GIF
- useful on day one
- friendly to both cloud AI users and local-first developers

## Roadmap

- [ ] improve scope detection
- [ ] add better message regeneration controls
- [ ] add provider-specific prompt tuning
- [ ] add optional commit body templates
- [ ] publish to PyPI
- [ ] ship terminal demo GIF

## 🤝 Contributing

PRs are welcome. Issues for provider support, prompt quality, and git edge cases are especially useful.

## 📝 License

MIT
