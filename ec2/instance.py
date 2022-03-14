from platform import release
from pprint import pprint
import boto3

def list_instance_ids() -> list:
    try:
        client = boto3.client('ec2')
        response = client.describe_instances(
            Filters=[
                {
                    'Name': 'instance-state-name',
                    'Values': [
                        'pending',
                        'running',
                        'stopping',
                        'stopped',
                    ]
                },
            ],
        )
        return [
            instance['InstanceId']
            for reservation in response['Reservations']
            for instance in reservation['Instances']
        ]
    except Exception as error:
        print(error)
        exit(1)

def terminate_instances(instance_ids: list) -> bool:
    try:
        client = boto3.client('ec2')
        client.terminate_instances(InstanceIds=instance_ids)
        waiter = client.get_waiter('instance_terminated')
        waiter.wait(InstanceIds=instance_ids)
        return True
    except Exception as error:
        print(error)
        exit(1)

class EC2InstanceResources:

    @classmethod
    async def init(cls):
        self = cls()
        self.instance_ids = list_instance_ids()
        return self
    
    def print(self):
        print("==== EC2 Instances ====")
        pprint(self.instance_ids)

    def delete(self):
        if self.instance_ids:
            terminate_instances(self.instance_ids)
            self.instance_ids = []