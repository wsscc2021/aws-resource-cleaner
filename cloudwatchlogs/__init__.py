from pprint import pprint
import boto3

def list_cloudwatch_log_group_names() -> list:
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
        # return successfully code, if done
        return True
    except Exception as error:
        print(error)
        exit(1)

class CloudWatchLogsResources:

    @classmethod
    async def init(cls):
        self = cls()
        self.cloudwatch_log_group_names = list_cloudwatch_log_group_names()
        return self
    
    def print(self):
        print("==== Cloudwatch Log Groups ====")
        pprint(self.cloudwatch_log_group_names)

    def delete(self):
        delete_cloudwatch_log_groups(self.cloudwatch_log_group_names)
        self.cloudwatch_log_group_names = []