from abc import ABC, abstractmethod

class StorageService(ABC):
    """ Abstract class for storage services """
    @abstractmethod
    def upload_file(self, file_path, destination):
        """ Upload a file to the storage service """
        pass

    @abstractmethod
    def download_file(self, source, destination):
        """ Download a file from the storage service """
        pass

    @abstractmethod
    def delete_file(self, file_path):
        """ Delete a file from the storage service """
        pass