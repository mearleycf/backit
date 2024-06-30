from abc import ABC, abstractmethod

class StorageService(ABC):
    @abstractmethod
    def configure_storage(self) -> None:
        """
        Configure and prepare the storage environment.
        """
        raise NotImplementedError

class ObjectStorageService(StorageService):
    """
    Interface for interactions with object storage services.
    """
    @abstractmethod
    def upload_file(self, file_path: str, destination: str) -> None:
        """
        Upload a file to the storage service.

        :param file_path: The local path to the file to be uploaded.
        :param destination: The destination path in the storage service.
        :type file_path: str
        :type destination: str
        """
        raise NotImplementedError

    @abstractmethod
    def download_file(self, source: str, destination: str) -> None:
        """
        Download a file from the storage service.

        :param source: The path in the storage service from where to download the file.
        :param destination: The local destination path where the file will be saved.
        :type source: str
        :type destination: str
        """
        raise NotImplementedError

    @abstractmethod
    def delete_file(self, file_path: str) -> None:
        """
        Delete a file from the storage service.

        :param file_path: The path to the file in the storage service that should be deleted.
        :type file_path: str
        """
        raise NotImplementedError

class VersionControlService(StorageService):
    """
    Interface for interactions with version control systems.
    """
    def create_branch(self, branch_name: str) -> None:
        """
        Create a new branch in the version control system.

        :param branch_name: The name of the new branch.
        :type branch_name: str
        """
        raise NotImplementedError

    def commit_changes(self, message: str) -> None:
        """
        Commit changes to the version control system with a commit message.

        :param message: The commit message describing the changes.
        :type message: str
        """
        raise NotImplementedError

    def push_changes(self) -> None:
        """
        Push committed changes to a remote repository.
        """
        raise NotImplementedError

    def pull_changes(self) -> None:
        """
        Pull changes from the remote repository.
        """
        raise NotImplementedError

    def merge_branch(self, source_branch: str, target_branch: str) -> None:
        """
        Merge one branch into another.

        :param source_branch: The name of the source branch.
        :param target_branch: The name of the target branch.
        :type source_branch: str
        :type target_branch: str
        """
        raise NotImplementedError