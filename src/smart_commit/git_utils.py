"""Git operations for SmartCommit."""
from pathlib import Path
from typing import List, Dict

from git import Repo, InvalidGitRepositoryError


class GitAnalyzer:
    """Analyzes git repository changes."""

    def __init__(self, repo_path: str = "."):
        try:
            self.repo = Repo(Path(repo_path).resolve(), search_parent_directories=True)
        except InvalidGitRepositoryError:
            raise ValueError("Not in a git repository")

    def get_staged_files(self) -> List[str]:
        """Get list of staged files."""
        diff = self.repo.index.diff("HEAD")
        return [item.a_path for item in diff]

    def get_staged_diff(self) -> str:
        """Get staged diff."""
        return self.repo.git.diff("--cached")

    def get_file_summary(self) -> List[Dict[str, str]]:
        """Get summary of changed files."""
        diff = self.repo.index.diff("HEAD", create_patch=True)
        summary = []
        for item in diff:
            # Count additions/deletions from patch
            patch = item.diff.decode("utf-8", errors="ignore")
            additions = sum(1 for line in patch.split("\n") if line.startswith("+") and not line.startswith("+++"))
            deletions = sum(1 for line in patch.split("\n") if line.startswith("-") and not line.startswith("---"))
            summary.append({
                "file": item.a_path,
                "additions": additions,
                "deletions": deletions,
                "change_type": item.change_type,
            })
        return summary

    def commit(self, message: str) -> None:
        """Create git commit with message."""
        self.repo.index.commit(message)
