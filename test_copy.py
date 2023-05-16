import boto3
import boto3.s3.transfer as s3transfer
from botocore.config import Config
s3_client = boto3.client("s3")


def s3_copy_init():
    global s3t
    transfer_config = s3transfer.TransferConfig(
        use_threads=True,
        max_concurrency=20,
    )
    s3t = s3transfer.create_transfer_manager(s3_client, transfer_config)


def s3_copy(src: dict, dest: dict) -> bool:
    if "s3t" not in globals():
        s3_copy_init()
    try:
        s3t.copy(copy_source=src, bucket=dest["Bucket"], key=dest["Key"])
    except Exception as e:
        if "cannot schedule new futures after shutdown" in e.args:
            print("Initiating and Retrying")
            s3_copy_init()
            s3_copy(src, dest)
        print(e)
        return False
    return True


