"""Configuration management for SmartCommit."""
import os
from pathlib import Path
from typing import Any, Optional

import yaml


class Config:
    """Configuration manager for SmartCommit."""

    DEFAULT_CONFIG = {
        "ai": {
            "provider": "openai",
            "model": "gpt-4o-mini",
            "temperature": 0.7,
        },
        "commit": {
            "style": "conventional",
            "max_length": 72,
            "include_scope": True,
        },
        "git": {
            "auto_stage": False,
            "auto_push": False,
        },
    }

    def __init__(self, config_path: Optional[Path] = None):
        self.config_path = config_path or self._get_config_path()
        self._config: dict = {}

    def _get_config_path(self) -> Path:
        """Get the config file path."""
        return Path.home() / ".smart-commit" / "config.yaml"

    def load(self) -> dict:
        """Load configuration from file."""
        if self.config_path.exists():
            with open(self.config_path) as f:
                self._config = yaml.safe_load(f) or {}
        else:
            self._config = self.DEFAULT_CONFIG.copy()
        return self._config

    def save(self) -> None:
        """Save configuration to file."""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, "w") as f:
            yaml.dump(self._config, f, default_flow_style=False)

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value using dot notation."""
        keys = key.split(".")
        value = self._config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
            if value is None:
                return default
        return value

    def set(self, key: str, value: Any) -> None:
        """Set a configuration value using dot notation."""
        keys = key.split(".")
        config = self._config
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value

    def ensure_api_key(self) -> bool:
        """Check if API key is configured."""
        provider = self.get("ai.provider", "openai")
        if provider == "openai":
            return bool(os.getenv("OPENAI_API_KEY"))
        elif provider == "anthropic":
            return bool(os.getenv("ANTHROPIC_API_KEY"))
        elif provider == "ollama":
            return bool(os.getenv("OLLAMA_HOST"))
        return False
