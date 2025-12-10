"""Wrapper around GitPython for Life.git tutorial"""

from pathlib import Path

from git import Repo
from git.exc import InvalidGitRepositoryError


class LifeRepo:
    """Abstraction over GitPython providing clean interface for tutorial operations"""

    def __init__(self, path: Path = Path.cwd()):
        self.path = path
        try:
            self.repo = Repo(path)
        except InvalidGitRepositoryError:
            self.repo = Repo.init(path)

    # Core operations

    def commit(self, message: str, files: list[str] | None = None):
        """Commit with optional file staging"""
        if files:
            self.repo.index.add(files)
        return self.repo.index.commit(message)

    def create_branch(self, name: str):
        """Create a new branch"""
        return self.repo.create_head(name)

    def checkout(self, branch: str):
        """Switch to a branch"""
        self.repo.heads[branch].checkout()

    def merge(self, branch: str):
        """Merge another branch into current"""
        return self.repo.git.merge(branch)

    # Validation helpers

    def count_commits(self, branch: str | None = None) -> int:
        """Count commits on a branch"""
        if not self.repo.heads:
            return 0
        ref = branch if branch else "HEAD"
        return len(list(self.repo.iter_commits(ref)))

    def get_last_commit_message(self) -> str:
        """Get the most recent commit message"""
        if not self.repo.heads:
            return ""
        return str(self.repo.head.commit.message).strip()

    def has_uncommitted_changes(self) -> bool:
        """Check for uncommitted changes (staged or unstaged)"""
        return self.repo.is_dirty(untracked_files=True)

    def has_untracked_files(self) -> bool:
        """Check for untracked files"""
        return len(self.repo.untracked_files) > 0

    def current_branch(self) -> str:
        """Get name of current branch"""
        if self.repo.head.is_detached:
            return "(detached HEAD)"
        return self.repo.active_branch.name

    def list_branches(self) -> list[str]:
        """Get all branch names"""
        return [head.name for head in self.repo.heads]

    def has_conflicts(self) -> bool:
        """Check if there are merge conflicts"""
        return len(self.repo.index.unmerged_blobs()) > 0

    def get_reflog(self, n: int = 10) -> list[str]:
        """Get recent reflog entries"""
        return self.repo.git.reflog(f"-{n}").split("\n")

    def file_in_last_commit(self, filename: str) -> bool:
        """Check if a file was modified in the last commit"""
        if not self.repo.heads:
            return False
        last_commit = self.repo.head.commit
        return filename in last_commit.stats.files

    def is_initialized(self) -> bool:
        """Check if repo has at least one commit"""
        return len(self.repo.heads) > 0
