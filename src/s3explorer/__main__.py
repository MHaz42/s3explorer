""" The main entrypoint module """

import os
import sys

# Insert source path in PYTHONPATH before importing s3explorer package
if not __package__:
    package_source_path = os.path.dirname(os.path.dirname(__file__))
    sys.path.insert(0, package_source_path)

import logging

from s3explorer.app import S3Explorer

def main():
    logging.info(f"Starting S3Explorer !!!")
    app = S3Explorer()
    app.run()


if __name__ == "__main__":
    main()
