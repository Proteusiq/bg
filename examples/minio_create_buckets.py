from os import environ
from decouple import config
from minio import Minio


# hide this load as .env
environ["AWS_ACCESS_KEY_ID"] = "danpra"
environ["AWS_SECRET_ACCESS_KEY"] = "miniopwd"

# Create client with access key and secret key with specific region.
client = Minio(
    "localhost:9000",
    access_key=config("AWS_ACCESS_KEY_ID"),
    secret_key=config("AWS_SECRET_ACCESS_KEY"),
    secure=False,
)


def create_bucket(bucket_name: str) -> bool:
    if not client.bucket_exists(bucket_name):

        client.make_bucket(bucket_name)

        return True
    return False


def delet_bucket(bucket_name: str) -> bool:
    if client.bucket_exists(bucket_name):

        client.remove_bucket(bucket_name)
        return True
    return False


if __name__ == "__main__":

    bucket_name = "example"
    status = create_bucket(bucket_name)
    print({"success": status})
