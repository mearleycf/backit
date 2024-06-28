from backit.services.storage_service import StorageService

class DigitalOceanStorage(StorageService):
    """ concrete implementation of StorageService for Digital Ocean """
    def upload_file(self, file_path, destination):
        # implement file upload logic here
        pass

    def download_file(self, file_path, destination):
        # implement file download logic here
        pass

    def delete_file(self, file_path):
        # implement file delete logic here
        pass