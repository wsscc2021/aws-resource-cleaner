from pprint import pprint
import boto3

def list_cloudwatch_log_groups() -> list:
    try:
        # init boto3
        client = boto3.client('logs')
        # describe all cloudwatch log groups in account
        response = client.describe_log_groups(logGroupNamePrefix='/')
        # parse and return log group name in above response
        return [ log_group['logGroupName'] for log_group in response['logGroups'] ]
    except Exception as error:
        print(error)
        exit(1)

def delete_cloudwatch_log_groups(cloudwatch_log_groups: list) -> bool:
    try:
        # init boto3
        client = boto3.client('logs')
        # delete all log groups
        for log_group in cloudwatch_log_groups:
            client.delete_log_group(logGroupName=log_group)
        # return successfully code, if done delete to all resources
        return True
    except Exception as error:
        print(error)
        exit(1)

def cloudwatch_logs_cleaner():
    try:
        # list up all resources at rds service
        cloudwatch_log_groups = list_cloudwatch_log_groups()

        # output will deleted resources list
        print("==== Cloudwatch Log Groups ====")
        pprint(cloudwatch_log_groups)

        # approval and delete all resources
        while True:
            confirm = input("Are you sure you want to delete (y/n)? ")
            if confirm == "y":
                delete_cloudwatch_log_groups(cloudwatch_log_groups)
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
    cloudwatch_logs_cleaner()
    print("done!")