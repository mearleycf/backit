from backit.services.storage_service import StorageService
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError
import os

class DigitalOceanStorage(StorageService):
    # concrete implementation of StorageService for Digital Ocean
    def __init__(self):
        self.client = boto3.client('s3', region_name='nyc3', endpoint_url='https://nyc3.digitaloceanspaces.com', aws_access_key_id=os.getenv('DIGITAL_OCEAN_ACCESS_KEY'), aws_secret_access_key=os.getenv('DIGITAL_OCEAN_SECRET_KEY'))

    def upload_file(self, file_path, destination):
        # upload a file to a Digital Ocean space
        try:
            self.client.upload_file(file_path, destination['bucket'], destination['key'])
            print(f"File uploaded to {destination['bucket']}/{destination['key']}")
        except (NoCredentialsError, PartialCredentialsError, ClientError) as e:
            print(f"Failed to upload file to {destination['bucket']}/{destination['key']}. Error: {e}")

    def download_file(self, file_path, destination):
        # implement file download logic here
        try:
            self.client.download_file(destination['bucket'], destination['key'], file_path)
            print(f"File downloaded successfully from {destination['bucket']}/{destination['key']} to {file_path}")
        except (ClientError) as e:
            print(f"Failed to download file from {destination['bucket']}/{destination['key']}. Error: {e}")

    def delete_file(self, destination):
        # implement file delete logic here
        try:
            self.client.delete_object(Bucket=destination['bucket'], Key=destination['key'])
            print(f"File deleted successfully from {destination['bucket']}/{destination['key']}")
        except (ClientError) as e:
            print(f"Failed to delete file from {destination['bucket']}/{destination['key']}. Error: {e}")