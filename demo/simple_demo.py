#!/usr/bin/env python3
"""Simple demo of SmartCommit."""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

print("SmartCommit Demo")
print("=" * 50)
print()
print("This demo shows how SmartCommit analyzes your git changes")
print("and generates commit messages.")
print()
print("To use SmartCommit:")
print("  1. git add <files>")
print("  2. smart-commit")
print("  3. Review and confirm")
print()
print("API Keys needed:")
print("  - OPENAI_API_KEY (OpenAI)")
print("  - ANTHROPIC_API_KEY (Claude)")
print("  - OLLAMA_HOST (Local, free)")
