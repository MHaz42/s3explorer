from pathlib import Path
from configparser import ConfigParser

import boto3


class S3:
    def __init__(self) -> None:
        self._read_config()

    def _read_config(self):
        config = ConfigParser()
        config.read(f"{Path.home()}/.s3cfg")
        self._s3_client = boto3.client(
            service_name="s3",
            endpoint_url=f"https://{config["default"]["host_base"]}",
            aws_access_key_id=config["default"]["access_key"],
            aws_secret_access_key=config["default"]["secret_key"],
        )

    def list_bucket(self):
        bucket_list = []
        for bucket in self._s3_client.list_buckets()["Buckets"]:
            bucket_list.append(bucket["Name"])
        return bucket_list

    def list_directory_content(self, bucket, path):
        directory_content = []
        result = self._s3_client.list_objects_v2(
            Bucket=bucket, Prefix=path, Delimiter="/"
        )
        for file in result.get("Contents", []):
            directory_content.append(
                {
                    "type": "file",
                    "key": file["Key"],
                    "size": file["Size"],
                    "last_modified": file["LastModified"],
                }
            )
        for directory in result.get("CommonPrefixes", []):
            directory_content.append(
                {
                    "type": "directory",
                    "key": directory["Prefix"].replace(path, "").strip("/"),
                }
            )
        return directory_content
