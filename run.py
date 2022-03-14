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

import asyncio

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
from cloudwatch import CloudwatchResources
import vpc

class AwsResources:

    @classmethod
    async def init(cls):
        self = cls()
        autoScalingGroupResources = AutoScalingGroupResources.init()
        rdsResources              = RDSResources.init()
        efsResources              = EFSResources.init()
        ec2InstanceResources      = EC2InstanceResources.init()
        loadBalancerResources     = LoadBalancerResources.init()
        securityGroupResources    = SecurityGroupResources.init()
        vpcResources              = VpcResources.init()
        eipResources              = EIPResources.init()
        s3Resources               = S3Resources.init()
        dynamodbResources         = DynamoDBResources.init()
        cloudWatchLogsResources   = CloudWatchLogsResources.init()
        cloudwatchResources       = CloudwatchResources.init()
        iamResources              = IAMResources.init()

        self.autoScalingGroupResources = await autoScalingGroupResources
        self.rdsResources              = await rdsResources
        self.efsResources              = await efsResources
        self.ec2InstanceResources      = await ec2InstanceResources
        self.loadBalancerResources     = await loadBalancerResources
        self.securityGroupResources    = await securityGroupResources
        self.vpcResources              = await vpcResources
        self.eipResources              = await eipResources
        self.s3Resources               = await s3Resources
        self.dynamodbResources         = await dynamodbResources
        self.cloudWatchLogsResources   = await cloudWatchLogsResources
        self.cloudwatchResources       = await cloudwatchResources
        self.iamResources              = await iamResources
        return self

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
        self.cloudwatchResources.print()
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
        self.cloudwatchResources.delete()
        self.iamResources.delete()


async def main():
    try:
        awsResources = await AwsResources.init()
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

if __name__ == '__main__':
    asyncio.run(main())