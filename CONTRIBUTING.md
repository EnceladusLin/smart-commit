# Contributing

Thanks for interest in SmartCommit!

## Development setup

```bash
git clone https://github.com/EnceladusLin/smart-commit.git
cd smart-commit
pip install -e .[dev]
```

## Running tests

```bash
pytest
```

## Code style

- Use ruff for linting
- Use type hints where helpful

## Adding new AI providers

1. Add provider class in `src/smart_commit/ai_provider.py`
2. Implement `generate(prompt: str, diff: str) -> str`
3. Register in CLI options

## Issues to explore

- prompt quality improvements
- better scope detection
- commit message style templates
- provider-specific tuning
