"""AI providers for SmartCommit."""
import os
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any

from openai import OpenAI
import anthropic


class AIProvider(ABC):
    """Base class for AI providers."""

    @abstractmethod
    def generate_commit_message(
        self,
        diff: str,
        file_summary: list,
        style: str = "conventional",
    ) -> str:
        """Generate commit message from diff."""
        pass


class OpenAIProvider(AIProvider):
    """OpenAI GPT provider."""

    def __init__(self, model: str = "gpt-4o-mini", temperature: float = 0.7):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not set")
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.temperature = temperature

    def generate_commit_message(
        self,
        diff: str,
        file_summary: list,
        style: str = "conventional",
    ) -> str:
        """Generate commit message using OpenAI."""
        summary_text = "\n".join(
            f"- {f['file']} ({f['change_type']}): +{f['additions']} -{f['deletions']}"
            for f in file_summary
        )

        prompt = self._build_prompt(diff, summary_text, style)

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an expert programmer who writes clear, concise git commit messages."},
                {"role": "user", "content": prompt}
            ],
            temperature=self.temperature,
        )

        return response.choices[0].message.content

    def _build_prompt(self, diff: str, summary: str, style: str) -> str:
        """Build prompt based on style."""
        base = f"""Analyze these git changes and generate a commit message.

Changed files:
{summary}

Diff:
{diff[:5000]}  # Limit diff length

Generate a {style} commit message. """

        if style == "conventional":
            base += """Use format: type(scope): description
- bullet point 1
- bullet point 2

Types: feat, fix, refactor, docs, style, test, chore, perf, ci, build"""
        elif style == "short":
            base += "Keep it under 50 characters."
        elif style == "detailed":
            base += "Include detailed explanation of what changed and why."

        return base


class AnthropicProvider(AIProvider):
    """Anthropic Claude provider."""

    def __init__(self, model: str = "claude-sonnet-4-6", temperature: float = 0.7):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not set")
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model
        self.temperature = temperature

    def generate_commit_message(
        self,
        diff: str,
        file_summary: list,
        style: str = "conventional",
    ) -> str:
        """Generate commit message using Claude."""
        summary_text = "\n".join(
            f"- {f['file']} ({f['change_type']}): +{f['additions']} -{f['deletions']}"
            for f in file_summary
        )

        prompt = self._build_prompt(diff, summary_text, style)

        response = self.client.messages.create(
            model=self.model,
            max_tokens=500,
            temperature=self.temperature,
            system="You are an expert programmer who writes clear, concise git commit messages.",
            messages=[{"role": "user", "content": prompt}]
        )

        return response.content[0].text

    def _build_prompt(self, diff: str, summary: str, style: str) -> str:
        """Build prompt based on style."""
        base = f"""Analyze these git changes and generate a commit message.

Changed files:
{summary}

Diff:
{diff[:5000]}

Generate a {style} commit message. """

        if style == "conventional":
            base += """Use format: type(scope): description
- bullet point 1
- bullet point 2

Types: feat, fix, refactor, docs, style, test, chore, perf, ci, build"""

        return base


class OllamaProvider(AIProvider):
    """Ollama local provider (free, privacy-first)."""

    def __init__(self, model: str = "codellama", temperature: float = 0.7):
        self.base_url = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        self.model = model
        self.temperature = temperature
        self.client = OpenAI(base_url=self.base_url + "/v1", api_key="ollama")

    def generate_commit_message(
        self,
        diff: str,
        file_summary: list,
        style: str = "conventional",
    ) -> str:
        """Generate commit message using Ollama."""
        summary_text = "\n".join(
            f"- {f['file']} ({f['change_type']}): +{f['additions']} -{f['deletions']}"
            for f in file_summary
        )

        prompt = f"""Analyze these git changes and generate a commit message.

Changed files:
{summary_text}

Diff:
{diff[:3000]}

Generate a {style} commit message. Use format: type(scope): description followed by bullet points."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=self.temperature,
            )
            return response.choices[0].message.content
        except Exception as e:
            raise RuntimeError(f"Ollama connection failed: {e}")


def get_provider(provider_name: str = "openai", **kwargs) -> AIProvider:
    """Get AI provider by name."""
    providers = {
        "openai": OpenAIProvider,
        "anthropic": AnthropicProvider,
        "ollama": OllamaProvider,
    }
    if provider_name not in providers:
        raise ValueError(f"Unknown provider: {provider_name}")
    return providers[provider_name](**kwargs)
