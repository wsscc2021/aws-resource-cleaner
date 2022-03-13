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
from ec2.instance import EC2InstanceResources
from elbv2.load_balancer import LoadBalancerResources
from ec2.security_group import SecurityGroupResources
from ec2.eip import EIPResources
from s3 import S3Resources

class AwsResources:

    def __init__(self):
        self.autoScalingGroupResources = AutoScalingGroupResources()
        self.ec2InstanceResources      = EC2InstanceResources()
        self.loadBalancerResources     = LoadBalancerResources()
        self.securityGroupResources    = SecurityGroupResources()
        self.vpcResources              = VpcResources()
        self.eipResources              = EIPResources()
        self.s3Resources               = S3Resources()

    def print(self):
        self.autoScalingGroupResources.print()
        self.ec2InstanceResources.print()
        self.loadBalancerResources.print()
        self.securityGroupResources.print()
        self.vpcResources.print()
        self.eipResources.print()
        self.s3Resources.print()
    
    def delete(self):
        self.autoScalingGroupResources.delete()
        self.ec2InstanceResources.delete()
        self.loadBalancerResources.delete()
        self.securityGroupResources.delete()
        self.vpcResources.delete()
        self.eipResources.delete()
        self.s3Resources.delete()


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