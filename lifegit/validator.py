"""Validation helpers for tutorial exercises"""

from pathlib import Path

from .git_wrapper import LifeRepo


class StageValidator:
    """Reusable validation logic for exercises"""

    @staticmethod
    def file_exists(filename: str, repo_path: Path = Path.cwd()) -> bool:
        """Check if file exists in working directory"""
        return (repo_path / filename).exists()

    @staticmethod
    def file_exists_and_committed(repo: LifeRepo, filename: str) -> bool:
        """Check if file exists and was included in the last commit"""
        if not StageValidator.file_exists(filename, repo.path):
            return False
        return repo.file_in_last_commit(filename)

    @staticmethod
    def branch_exists(repo: LifeRepo, branch_name: str) -> bool:
        """Check if a branch exists"""
        return branch_name in repo.list_branches()

    @staticmethod
    def on_branch(repo: LifeRepo, branch_name: str) -> bool:
        """Check if currently on a specific branch"""
        return repo.current_branch() == branch_name

    @staticmethod
    def has_commits(repo: LifeRepo, minimum: int = 1) -> bool:
        """Check if repo has at least minimum number of commits"""
        return repo.count_commits() >= minimum

    @staticmethod
    def branches_merged(repo: LifeRepo, source: str, target: str) -> bool:
        """Check if source branch is merged into target"""
        if source not in repo.list_branches():
            return False
        if target not in repo.list_branches():
            return False

        # Check if source's tip commit is in target's history
        source_commit = repo.repo.heads[source].commit
        target_commits = list(repo.repo.iter_commits(target))
        return source_commit in target_commits

    @staticmethod
    def conflict_resolved(repo: LifeRepo) -> bool:
        """Check if merge conflicts are resolved"""
        return not repo.has_conflicts() and not repo.has_uncommitted_changes()
