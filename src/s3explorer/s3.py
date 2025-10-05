from pathlib import Path
from configparser import ConfigParser
from typing import Dict

import boto3

from s3explorer.entities import FileDescription, FileType


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
        directory_content: Dict[str, FileDescription] = {}
        result = self._s3_client.list_objects_v2(
            Bucket=bucket, Prefix=path, Delimiter="/"
        )
        print(result)
        if path != "":
            directory_content[".."] = FileDescription(FileType.RETURN)
        for file in result.get("Contents", []):
            directory_content[file["Key"].replace(path, "")] = FileDescription(
                FileType.FILE, file["Size"], file["LastModified"]
            )
        for directory in result.get("CommonPrefixes", []):
            directory_content[directory["Prefix"].replace(path, "").strip("/")] = (
                FileDescription(FileType.DIRECTORY)
            )

        return directory_content
