# 🧠 SmartCommit

> AI-powered git commit message generator that writes your commit messages for you.

[![PyPI Version](https://img.shields.io/pypi/v/smart-commit.svg)](https://pypi.org/project/smart-commit/)
[![Python Versions](https://img.shields.io/pypi/pyversions/smart-commit.svg)](https://pypi.org/project/smart-commit/)
[![License](https://img.shields.io/pypi/l/smart-commit.svg)](LICENSE)

**SmartCommit** analyzes your staged git changes and generates meaningful, conventional commit messages using AI. No more staring at a blank terminal wondering how to summarize your changes.

## ✨ Features

- 🚀 **One-command** commit message generation
- 📝 **Conventional Commits** format by default
- 🤖 **Multiple AI providers**: OpenAI, Anthropic Claude, Ollama (local)
- ⚡ **Fast**: Only analyzes staged changes, not entire repo
- 🔒 **Privacy-first**: Your code never leaves your machine (local mode available)
- 🎨 **Customizable**: Configure style, format, and behavior
- 📦 **Works offline** with local AI (Ollama)

## 📋 Requirements

- Python 3.8+
- Git
- At least one AI provider configured (see below)

## 🛠️ Installation

```bash
# From PyPI
pip install smart-commit

# Or from source
pip install git+https://github.com/yourusername/smart-commit.git
```

## 🔧 Configuration

### Option 1: OpenAI

```bash
export OPENAI_API_KEY="sk-..."
```

### Option 2: Anthropic Claude

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

### Option 3: Ollama (Local, Free)

```bash
# Install Ollama first: https://github.com/ollama/ollama
ollama pull codellama
export OLLAMA_HOST="http://localhost:11434"
```

### First Run

```bash
smart-commit init
```

This creates `~/.smart-commit/config.yaml` with default settings.

## 🎯 Usage

### Basic Workflow

```bash
# Stage your changes
git add .

# Generate commit message
smart-commit

# Or with short flag
sc
```

### Example Output

```
 Analyzing 3 staged files...
 ✓ Analyzed src/auth.py (+45, -12)
 ✓ Analyzed tests/test_auth.py (+28, -5)
 ✓ Analyzed README.md (+3, -1)

🤖 Generating commit message...

Suggested commit message:
---
feat(auth): add JWT token refresh mechanism

- Implement refresh_token endpoint in /auth/refresh
- Add token expiration check before validation
- Update test cases for new refresh flow
- Fix typo in README auth section
---

Options: [y] Accept  [e] Edit  [r] Regenerate  [a] Abort
>
```

### Advanced Usage

```bash
# Use specific AI provider
smart-commit --provider openai
smart-commit --provider anthropic
smart-commit --provider ollama

# Custom style
smart-commit --style "short,emoji"
smart-commit --style "conventional"
smart-commit --style "detailed"

# Dry run (show message without committing)
smart-commit --dry-run

# Edit message before commit
smart-commit --edit
```

## 📖 Configuration File

Location: `~/.smart-commit/config.yaml`

```yaml
ai:
  provider: openai  # openai, anthropic, ollama
  model: gpt-4o-mini
  temperature: 0.7

commit:
  style: conventional  # conventional, short, detailed, emoji
  max_length: 72
  include_scope: true

git:
  auto_stage: false
  auto_push: false
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

MIT License - see [LICENSE](LICENSE) for details.

---

**Made with 🔥 by developers, for developers**
