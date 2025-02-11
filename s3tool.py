from phi.tools import Toolkit

try:
    import boto3
except ImportError:
    raise ImportError("boto3 is required for S3Tool. Please install it using `pip install boto3`.")


class S3Tool(Toolkit):
    name: str = "S3Tool"
    description: str = "A tool for interacting with AWS S3 buckets"

    def __init__(self, region_name: str = "YOUR_REGION"):
        super().__init__()
        self.client = boto3.client("s3", region_name=region_name)
        self.register(self.list_buckets)
        self.register(self.upload_file)
        self.register(self.download_file)

    def list_buckets(self) -> str:
        try:
            response = self.client.list_buckets()
            buckets = [bucket["Name"] for bucket in response["Buckets"]]
            return f"Available S3 buckets: {', '.join(buckets)}"
        except Exception as e:
            return f"Error listing buckets: {str(e)}"

    def upload_file(self, bucket_name: str, file_path: str, object_key: str) -> str:
        try:
            self.client.upload_file(file_path, bucket_name, object_key)
            return f"File uploaded successfully to bucket: {bucket_name}, key: {object_key}"
        except Exception as e:
            return f"Error uploading file: {str(e)}"

    def download_file(self, bucket_name: str, object_key: str, file_path: str) -> str:
        try:
            self.client.download_file(bucket_name, object_key, file_path)
            return f"File downloaded successfully from bucket: {bucket_name}, key: {object_key}, to: {file_path}"
        except Exception as e:
            return f"Error downloading file: {str(e)}"
