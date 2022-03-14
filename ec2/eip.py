from pprint import pprint
import boto3

def list_idle_eip_allocation_ids() -> list:
    try:
        client = boto3.client('ec2')
        response = client.describe_addresses()
        return [
            address['AllocationId']
            for address in response['Addresses']
            if 'AssociationId' not in address
        ]
    except Exception as error:
        print(error)
        exit(1)

def release_eip_addresses(eip_allocation_ids: list) -> bool:
    try:
        client = boto3.client('ec2')
        for eip_allocation_id in eip_allocation_ids:
            client.release_address(AllocationId=eip_allocation_id)
        return True
    except Exception as error:
        print(error)
        exit(1)

class EIPResources:

    @classmethod
    async def init(cls):
        self = cls()
        self.eip_allocation_ids = list_idle_eip_allocation_ids()
        return self

    def print(self):
        print("==== Idle EIP Addresses ====")
        pprint(self.eip_allocation_ids)

    def delete(self):
        if self.eip_allocation_ids:
            release_eip_addresses(self.eip_allocation_ids)
            self.eip_allocation_ids = []