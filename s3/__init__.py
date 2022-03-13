from pprint import pprint
import boto3

def list_bucket_names() -> list:
    try:
        # init boto3
        client = boto3.client('s3')
        # list all buckets in account
        response = client.list_buckets()
        # parse and return bucket names from repsonse
        return [ bucket['Name'] for bucket in response['Buckets'] ]
    except Exception as error:
        print(error)
        exit(1)

def empty_buckets(buckets: list) -> bool:
    try:
        # init boto3
        s3 = boto3.resource('s3')
        # delete all objects in each bucket
        for bucket in buckets:
            s3.Bucket(bucket).object_versions.delete()
        # return successfully code, if done
        return True
    except Exception as error:
        print(error)
        exit(1)

def delete_buckets(bucket_names: list) -> bool:
    try:
        # init boto3
        client = boto3.client('s3')
        # delete all buckets
        for bucket in bucket_names:
            client.delete_bucket(Bucket=bucket)
        # return successfully code, if done
        return True
    except Exception as error:
        print(error)
        exit(1)

class S3Resources:

    def __init__(self):
        self.bucket_names = list_bucket_names()

    def print(self):
        # output will deleted resources list
        print("==== S3 Buckets ====")
        pprint(self.bucket_names)
    
    def delete(self):
        empty_buckets(self.bucket_names)
        delete_buckets(self.bucket_names)
        self.bucket_names = []