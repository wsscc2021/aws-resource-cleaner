from pprint import pprint
import boto3

def list_buckets() -> list:
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
            s3.Bucket(bucket).objects.all().delete()
        # return successfully code, if done delete to all resources
        return True
    except Exception as error:
        print(error)
        exit(1)

def delete_buckets(buckets: list) -> bool:
    try:
        # init boto3
        client = boto3.client('s3')
        # delete all buckets
        for bucket in buckets:
            client.delete_bucket(Bucket=bucket)
        # return successfully code, if done delete to all resources
        return True
    except Exception as error:
        print(error)
        exit(1)

def s3_cleaner():
    try:
        buckets = list_buckets()
        print("==== S3 Buckets ====")
        pprint(buckets)
        while True:
            confirm = input("Are you sure you want to delete (y/n)? ")
            if confirm == "y":
                empty_buckets(buckets)
                delete_buckets(buckets)
                return True
            elif confirm == "n":
                print("Canceled")
                exit(1)
            else:
                print("Only input 'y' or 'n', Try again! ")
    except Exception as error:
        print(error)
        exit(1)

if __name__ == '__main__':
    s3_cleaner()
    print("done!")