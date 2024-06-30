class ObjectStorageService:
    """
    Interface for interactions with object storage services.
    """

    def upload_file(self, file_path, destination):
        raise NotImplementedError

    def download_file(self, file_path, destination):
        raise NotImplementedError

    def delete_file(self, file_path):
        raise NotImplementedError

class VersionControlService:
    """
    Interface for interactions with version control systems.
    """

    def commit_changes(self, message):
        raise NotImplementedError

    def push_changes(self):
        raise NotImplementedError

    def pull_changes(self):
        raise NotImplementedError

    def create_branch(self, branch_name):
        raise NotImplementedError

    def merge_branch(self, source_branch, target_branch):
        raise NotImplementedError