from pprint import pprint
import boto3

def list_security_group_ids() -> list:
    try:
        # init boto3 client
        client = boto3.client('ec2')
        # describe all security groups
        response = client.describe_security_groups()
        # parse and return security group ids from above response
        # it exclude default security group
        return [ 
            security_group['GroupId']
            for security_group in response['SecurityGroups']
            if security_group['GroupName'] != 'default' ]
    except Exception as error:
        print(error)
        exit(1)

def revoke_security_group_rules(security_group_ids: list) -> list:
    try:
        # init boto3 client
        client = boto3.client('ec2')
        # describe all security group rules
        response = client.describe_security_group_rules(
            Filters=[
                {
                    'Name': 'group-id',
                    'Values': security_group_ids
                }
            ])
        security_group_rules = response['SecurityGroupRules']
        # revoke all security group rules
        for security_group_id in security_group_ids:
            egress_rule_ids = [
                security_group_rule['SecurityGroupRuleId']
                for security_group_rule in security_group_rules
                if security_group_rule['GroupId'] == security_group_id and security_group_rule['IsEgress']
            ]
            ingress_rule_ids = [
                security_group_rule['SecurityGroupRuleId']
                for security_group_rule in security_group_rules
                if security_group_rule['GroupId'] == security_group_id and not security_group_rule['IsEgress']
            ]
            if egress_rule_ids: client.revoke_security_group_egress(
                GroupId=security_group_id,
                SecurityGroupRuleIds=egress_rule_ids)
            if ingress_rule_ids: client.revoke_security_group_ingress(
                GroupId=security_group_id,
                SecurityGroupRuleIds=ingress_rule_ids)
        # return successfully code, if done.
        return True
    except Exception as error:
        print(error)
        exit(1)

def delete_security_groups(security_group_ids: list) -> bool:
    try:
        # init boto3 client
        client = boto3.client('ec2')
        # delete security groups
        for security_group_id in security_group_ids:
            client.delete_security_group(GroupId=security_group_id)
        # if successfully code, if done.
        return True
    except Exception as error:
        print(error)
        exit(1)

class SecurityGroupResources:

    def __init__(self):
        self.security_group_ids = list_security_group_ids()
    
    def print(self):
        print("==== EC2 Security Groups ====")
        pprint(self.security_group_ids)
    
    def delete(self):
        revoke_security_group_rules(self.security_group_ids)
        delete_security_groups(self.security_group_ids)