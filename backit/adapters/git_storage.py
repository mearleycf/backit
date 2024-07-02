from backit.services.storage_service import StorageService
from backit.utils.file_utils import ensure_dir_exists
from git import Repo, GitCommandError
import os
import shutil
import uuid
from datetime import datetime
from urllib.parse import urlparse

class GitStorage(StorageService):
    """
    Concrete implementation of StorageService for Git.
    Manages operations related to a git repository for backing up files.
    """

    def __init__(self, backup_repo_path, remote_url, timestamp_format):
        self.timestamp_format = timestamp_format
        self.backup_repo_path = backup_repo_path
        self.remote_url = remote_url

    def config_repository(self):
        """
        Configures the repository by ensuring the repository directory exists,
        initializing the repository if necessary, and setting up the remote URL.
        """
        ensure_dir_exists(self.backup_repo_path)

        try:
            repo = Repo(self.backup_repo_path)
        except GitCommandError:
            repo = Repo.init(self.backup_repo_path)

        parsed_url = urlparse(self.remote_url)
        if parsed_url.scheme and parsed_url.netloc:
            if 'origin' not in repo.remotes:
                repo.create_remote('origin', self.remote_url)
        else:
            raise ValueError(f"{self.remote_url} is not a valid remote URL.")

    @classmethod
    def create_and_configure(cls, backup_repo_path, remote_url, timestamp_format):
        """
        Factory method to create and configure a GitStorage instance.
        Args:
            backup_repo_path (str): Path to the local git repository.
            remote_url (str): URL of the remote git repository.
            timestamp_format (str): Format string for timestamp in filenames.
        Returns:
            GitStorage: An instance of GitStorage configured with the given parameters.
        """
        storage = cls(backup_repo_path, remote_url, timestamp_format)
        storage.config_repository()
        return storage

# Usage:
git_storage = GitStorage.create_and_configure(
    backup_repo_path='/path/to/backup/repo',
    remote_url='https://github.com/username/repo.git',
    timestamp_format='%Y-%m-%d_%H-%M-%S'
)