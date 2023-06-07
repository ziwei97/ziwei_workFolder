import boto3.s3.transfer as s3transfer
import boto3
import atexit



def s3_copy(src: dict, dest: dict):
    s3 = boto3.client('s3')
    transfer_config = s3transfer.TransferConfig(
        use_threads=True,
        max_concurrency=20,
    )
    s3_tran = s3transfer.create_transfer_manager(s3, transfer_config)
    try:
        s3_tran.copy(copy_source=src, bucket=dest['Bucket'], key=dest['Key'])
    except Exception as err:
        print(err)












