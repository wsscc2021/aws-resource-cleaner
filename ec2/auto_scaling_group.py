from pprint import pprint
import boto3
import time

def list_auto_scaling_group_names() -> list:
    try:
        client = boto3.client('autoscaling')
        response = client.describe_auto_scaling_groups()
        return [ asg['AutoScalingGroupName'] for asg in response['AutoScalingGroups'] ]
    except Exception as error:
        print(error)
        exit(1)

def empty_auto_scaling_groups(auto_scaling_group_names: list) -> bool:
    try:
        client = boto3.client('autoscaling')
        for auto_scaling_group_name in auto_scaling_group_names:
            client.update_auto_scaling_group(
                AutoScalingGroupName=auto_scaling_group_name,
                MinSize=0,
                MaxSize=0,
                DesiredCapacity=0)
        waiter = boto3.client('ec2').get_waiter('instance_terminated')
        waiter.wait(
            Filters=[
                {
                    'Name': 'tag:aws:autoscaling:groupName',
                    'Values': auto_scaling_group_names
                },
            ],
        )
        time.sleep(5)
        return True
    except Exception as error:
        print(error)
        exit(1)

def delete_auto_scaling_groups(auto_scaling_group_names: list) -> bool:
    try:
        client = boto3.client('autoscaling')
        for auto_scaling_group_name in auto_scaling_group_names:
            client.delete_auto_scaling_group(
                AutoScalingGroupName=auto_scaling_group_name,
                ForceDelete=False)
        return True
    except Exception as error:
        print(error)
        exit(1)

def list_launch_template_names() -> list:
    try:
        client = boto3.client('ec2')
        response = client.describe_launch_templates()
        return [ launch_template['LaunchTemplateName'] for launch_template in response['LaunchTemplates'] ]
    except Exception as error:
        print(error)
        exit(1)

def delete_launch_templates(launch_template_names: list) -> bool:
    try:
        client = boto3.client('ec2')
        for launch_template_name in launch_template_names:
            client.delete_launch_template(LaunchTemplateName=launch_template_name)
        return True
    except Exception as error:
        print(error)
        exit(1)

class AutoScalingGroupResources:

    @classmethod
    async def init(cls):
        self = cls()
        self.auto_scaling_group_names = list_auto_scaling_group_names()
        self.launch_template_names    = list_launch_template_names()
        return self

    def print(self):
        # print list of resources.
        print("==== EC2 Auto Scaling Groups ====")
        pprint(self.auto_scaling_group_names)
        print("==== EC2 Launch Templates ====")
        pprint(self.launch_template_names)

    def delete(self):
        # delete resources in aws account.
        if self.auto_scaling_group_names:
            empty_auto_scaling_groups(self.auto_scaling_group_names)
            delete_auto_scaling_groups(self.auto_scaling_group_names)
        if self.launch_template_names:
            delete_launch_templates(self.launch_template_names)