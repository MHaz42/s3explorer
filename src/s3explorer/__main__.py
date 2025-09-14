""" The main entrypoint module """

from s3explorer.app import S3Explorer

def main():
    app = S3Explorer()
    app.run()


if __name__ == "__main__":
    main()
