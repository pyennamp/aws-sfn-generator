from utils.logger import log
import boto3
import sys


def split_s3_path(s3_path):
    """Returns bucket and key from s3 location"""
    path_parts = s3_path.replace("s3://", "").split("/")
    bucket = path_parts.pop(0)
    key = "/".join(path_parts)
    return bucket, key


def check_s3_files(file_list: str, path: str):
    """This function checks if a file exists in s3"""
    files = file_list.split(";")
    s3_client = boto3.client('s3')
    for file in files:
        try:
            file_path = path + file
            log.info("Checking file_path for - " + file_path + " has started")
            bucket, key = split_s3_path(file_path)
            s3_client.head_object(Bucket=bucket, Key=key)
            log.info("Checking file_path for - " + file_path + " has completed")
        except Exception as e:
            log.error("File check failed due to the mentioned exception - " + str(e))
            sys.exit(1)
    return True


def lambda_handler(event, context):
    try:
        file_list = event['file_list']
        ind_file_path = event['ind_file_path']
        check_s3_files(file_list, ind_file_path)
    except Exception as e:
        log.error('Lambda processor Failed - ' + str(e))
        sys.exit(1)
