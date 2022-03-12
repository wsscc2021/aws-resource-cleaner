from pprint import pprint
import boto3
import time

def list_load_balancer_arns() -> list:
    try:
        client = boto3.client('elbv2')
        response = client.describe_load_balancers()
        return [
            load_balancer['LoadBalancerArn']
            for load_balancer in response['LoadBalancers']
        ]
    except Exception as error:
        print(error)
        exit(1)

def delete_load_balancers(load_balancer_arns: list) -> bool:
    try:
        pass
        client = boto3.client('elbv2')
        for load_balancer_arn in load_balancer_arns:
            client.delete_load_balancer(LoadBalancerArn=load_balancer_arn)
        waiter = client.get_waiter('load_balancers_deleted')
        waiter.wait(LoadBalancerArns=load_balancer_arns)
        time.sleep(3)
        return True
    except Exception as error:
        print(error)
        exit(1)

def list_target_group_arns() -> list:
    try:
        client = boto3.client('elbv2')
        response = client.describe_target_groups()
        return [
            target_group['TargetGroupArn']
            for target_group in response['TargetGroups']
        ]
    except Exception as error:
        print(error)
        exit(1)

def delete_target_groups(target_group_arns: list) -> bool:
    try:
        client = boto3.client('elbv2')
        for target_group_arn in target_group_arns:
            client.delete_target_group(TargetGroupArn=target_group_arn)
        return True
    except Exception as error:
        print(error)
        exit(1)

class LoadBalancerResources:

    def __init__(self):
        self.load_balancer_arns = list_load_balancer_arns()
        self.target_group_arns = list_target_group_arns()
    
    def print(self):
        # output will deleted resources list
        print("==== Elastic Load Balancers ====")
        pprint(self.load_balancer_arns)
        print("==== Target Groups ====")
        pprint(self.target_group_arns)
    
    def delete(self):
        # delete load balancer
        if self.load_balancer_arns:
            delete_load_balancers(self.load_balancer_arns)
            self.load_balancer_arns = []
        # delete target groups
        if self.target_group_arns:
            delete_target_groups(self.target_group_arns)
            self.load_balancer_arns = []