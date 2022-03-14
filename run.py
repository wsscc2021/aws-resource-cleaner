# order of deleting resources
# auto-scaling-group, rds, efs
# ↓
# instances
# ↓
# elb
# ↓
# security-group
# ↓
# vpc
# ↓
# eip
# ↓
# s3, iam, cloudwatchlogs

from vpc import VpcResources
from ec2.auto_scaling_group import AutoScalingGroupResources
from rds import RDSResources
from efs import EFSResources
from ec2.instance import EC2InstanceResources
from elbv2.load_balancer import LoadBalancerResources
from ec2.security_group import SecurityGroupResources
from ec2.eip import EIPResources
from s3 import S3Resources
from iam import IAMResources
from dynamodb import DynamoDBResources
from cloudwatchlogs import CloudWatchLogsResources

class AwsResources:

    def __init__(self):
        self.autoScalingGroupResources = AutoScalingGroupResources()
        self.rdsResources              = RDSResources()
        self.efsResources              = EFSResources()
        self.ec2InstanceResources      = EC2InstanceResources()
        self.loadBalancerResources     = LoadBalancerResources()
        self.securityGroupResources    = SecurityGroupResources()
        self.vpcResources              = VpcResources()
        self.eipResources              = EIPResources()
        self.s3Resources               = S3Resources()
        self.dynamodbResources         = DynamoDBResources()
        self.cloudWatchLogsResources   = CloudWatchLogsResources()
        self.iamResources              = IAMResources()

    def print(self):
        self.autoScalingGroupResources.print()
        self.rdsResources.print()
        self.efsResources.print()
        self.ec2InstanceResources.print()
        self.loadBalancerResources.print()
        self.securityGroupResources.print()
        self.vpcResources.print()
        self.eipResources.print()
        self.s3Resources.print()
        self.dynamodbResources.print()
        self.cloudWatchLogsResources.print()
        self.iamResources.print()
    
    def delete(self):
        self.autoScalingGroupResources.delete()
        self.rdsResources.delete()
        self.efsResources.delete()
        self.ec2InstanceResources.delete()
        self.loadBalancerResources.delete()
        self.securityGroupResources.delete()
        self.vpcResources.delete()
        self.eipResources.delete()
        self.s3Resources.delete()
        self.dynamodbResources.delete()
        self.cloudWatchLogsResources.delete()
        self.iamResources.delete()


if __name__ == '__main__':
    try:
        awsResources = AwsResources()
        awsResources.print()
        while True:
            confirm = input("Are you sure you want to delete (y/n)? ")
            if confirm == "y":
                awsResources.delete()
                print("Done!")
                exit(0)
            elif confirm == "n":
                print("Canceled")
                exit(1)
            else:
                print("Only input 'y' or 'n', Try again! ")
    except Exception as error:
        print(error)
        exit(1)