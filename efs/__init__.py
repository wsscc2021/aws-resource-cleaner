from pprint import pprint
import boto3

def list_file_systems() -> list:
    try:
        # init boto3 client
        client = boto3.client('efs')
        # describe all file systems
        response = client.describe_file_systems()
        # parse and return file system ids from above response
        return [ file_system['FileSystemId']  for file_system in response['FileSystems'] ]
    except Exception as error:
        print(error)
        exit(1)

def list_mount_targets(file_system: str) -> list:
    try:
        client = boto3.client('efs')
        response = client.describe_mount_targets(FileSystemId=file_system)
        return [ mount_target['MountTargetId'] for mount_target in response['MountTargets'] ]
    except Exception as error:
        print(error)
        exit(1)

def delete_mount_targets(mount_targets: list) -> bool:
    try:
        client = boto3.client('efs')
        for mount_target in mount_targets:
            client.delete_mount_target(MountTargetId=mount_target)
        return True
    except Exception as error:
        print(error)
        exit(1)

def delete_file_systems(file_systems: list) -> bool:
    try:
        # init boto3 client
        client = boto3.client('efs')
        # delete file systems
        for file_system in file_systems:
            mount_targets = list_mount_targets(file_system)
            delete_mount_targets(mount_targets)
            # need for waiter delete target mounts
            client.delete_file_system(FileSystemId=file_system)
        # return successfully code, if done
        return True
    except Exception as error:
        print(error)
        exit(1)


class EFSResources:

    def __init__(self):
        self.file_systems = list_file_systems()

    def print(self):
        print("==== EFS File Systems ====")
        pprint(self.file_systems)

    def delete(self):
        delete_file_systems(self.file_systems)
        self.file_systems = []