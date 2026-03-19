"""Tests for SmartCommit."""
import os
import pytest
from unittest.mock import patch, MagicMock

from smart_commit.config import Config
from smart_commit.git_utils import GitAnalyzer
from smart_commit.ai_provider import OpenAIProvider, AnthropicProvider, OllamaProvider


class TestConfig:
    """Tests for configuration management."""

    def test_default_config(self):
        """Test default configuration values."""
        cfg = Config()
        cfg.load()
        assert cfg.get("ai.provider") == "openai"
        assert cfg.get("ai.model") == "gpt-4o-mini"
        assert cfg.get("commit.style") == "conventional"

    def test_config_get_nested(self):
        """Test nested config retrieval."""
        cfg = Config()
        cfg.load()
        assert cfg.get("ai.temperature") == 0.7

    def test_config_set(self):
        """Test setting config values."""
        cfg = Config()
        cfg.load()
        cfg.set("ai.provider", "anthropic")
        assert cfg.get("ai.provider") == "anthropic"


class TestGitAnalyzer:
    """Tests for git operations."""

    @patch('smart_commit.git_utils.Repo')
    def test_get_staged_files(self, mock_repo):
        """Test getting staged files."""
        mock_diff = MagicMock()
        mock_diff.a_path = "test.py"
        mock_repo.return_value.index.diff.return_value = [mock_diff]
        
        analyzer = GitAnalyzer(".")
        files = analyzer.get_staged_files()
        assert "test.py" in files

    @patch('smart_commit.git_utils.Repo')
    def test_get_file_summary(self, mock_repo):
        """Test getting file change summary."""
        mock_item = MagicMock()
        mock_item.a_path = "test.py"
        mock_item.change_type = "M"
        mock_item.diff = b"--- a/test.py\n+++ b/test.py\n+print('hello')\n"
        
        mock_repo.return_value.index.diff.return_value = [mock_item]
        
        analyzer = GitAnalyzer(".")
        summary = analyzer.get_file_summary()
        assert len(summary) > 0
        assert summary[0]["file"] == "test.py"


class TestAIProviders:
    """Tests for AI providers."""

    @patch('smart_commit.ai_provider.OpenAI')
    def test_openai_provider(self, mock_openai):
        """Test OpenAI provider."""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(message=MagicMock(content="feat: test commit"))]
        mock_openai.return_value.chat.completions.create.return_value = mock_response
        
        provider = OpenAIProvider(model="gpt-4o-mini")
        result = provider.generate_commit_message(
            diff="+print('hello')",
            file_summary=[{"file": "test.py", "additions": 1, "deletions": 0, "change_type": "M"}],
            style="conventional"
        )
        assert "feat" in result.lower() or "test" in result.lower()

    def test_ollama_provider_requires_host(self):
        """Test Ollama requires host configuration."""
        with pytest.raises(Exception):
            # Should fail without OLLAMA_HOST
            provider = OllamaProvider()
            # Will raise on connection attempt


class TestCLI:
    """Tests for CLI interface."""

    def test_cli_help(self):
        """Test CLI help output."""
        from smart_commit.cli import main
        from click.testing import CliRunner
        
        runner = CliRunner()
        result = runner.invoke(main, ['--help'])
        assert result.exit_code == 0
        assert 'SmartCommit' in result.output
