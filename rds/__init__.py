from pprint import pprint
import boto3
import botocore

client = boto3.client('rds')

def list_db_instances() -> list:
    try:
        # init boto3 client
        client = boto3.client('rds')
        # describe all db instances
        response = client.describe_db_instances()
        # parse and return db instance identifiers from above response
        return [ db_instance['DBInstanceIdentifier'] for db_instance in response['DBInstances'] ]
    except Exception as error:
        print(error)
        exit(1)


def list_db_clusters() -> list:
    try:
        # init boto3 client
        client = boto3.client('rds')
        # describe all db clusters
        response = client.describe_db_clusters()
        # parse and return db cluster identifier from above response
        return [ db_cluster['DBClusterIdentifier'] for db_cluster in response['DBClusters'] ]
    except Exception as error:
        print(error)
        exit(1)

def list_subnet_groups() -> list:
    try:
        # init boto3 client
        client = boto3.client('rds')
        # describe all subnet groups
        response = client.describe_db_subnet_groups()
        # parse and return subnet group names from above response
        return [ subnet_group['DBSubnetGroupName'] for subnet_group in response['DBSubnetGroups'] ]
    except Exception as error:
        print(error)
        exit(1)

def list_parameter_groups() -> list:
    try:
        # init boto3 client
        client = boto3.client('rds')
        # describe all parameter groups
        response = client.describe_db_parameter_groups()
        # parse and return parameter group names from above response
        # it exclude default parameter groups
        return [
            parameter_group['DBParameterGroupName']
            for parameter_group in response['DBParameterGroups']
            if parameter_group['DBParameterGroupName'].split('.')[0] != 'default' ]
    except Exception as error:
        print(error)
        exit(1)

def list_cluster_parameter_groups() -> list:
    try:
        # init boto3 client
        client = boto3.client('rds')
        # describe all cluster parameter groups
        response = client.describe_db_cluster_parameter_groups()
        # parse and return cluster parameter group names from above response
        # it exclude default cluster paramter groups
        return [
            parameter_group['DBClusterParameterGroupName']
            for parameter_group in response['DBClusterParameterGroups']
            if parameter_group['DBClusterParameterGroupName'].split('.')[0] != 'default' ]
    except Exception as error:
        print(error)
        exit(1)

def delete_db_instances(db_instances: list) -> bool:
    try:
        # init boto3 client
        client = boto3.client('rds')
        # delete db instances
        for db_instance in db_instances:
            client.delete_db_instance(
                DBInstanceIdentifier=db_instance,
                SkipFinalSnapshot=True,
                DeleteAutomatedBackups=True)
        # wait for completed delete db instances
        client.get_waiter('db_instance_deleted').wait()
        # return successfully code, if done.
        return True
    except Exception as error:
        print(error)
        exit(1)

def delete_db_clusters(db_clusters: list) -> bool:
    try:
        # init boto3 client
        client = boto3.client('rds')
        # delete db clusters
        for db_cluster in db_clusters:
            client.delete_db_cluster(
                DBClusterIdentifier=db_cluster,
                SkipFinalSnapshot=True)
        # return successfully code, if done.
        return True
    except Exception as error:
        print(error)
        exit(1)

def delete_subnet_groups(subnet_groups: list) -> bool:
    try:
        # init boto3 client
        client = boto3.client('rds')
        # delete subnet groups
        for subnet_group in subnet_groups:
            client.delete_db_subnet_group(DBSubnetGroupName=subnet_group)
        # return successfully code, if done.
        return True
    except Exception as error:
        print(error)
        exit(1)

def delete_parameter_groups(parameter_groups: list) -> bool:
    try:
        # init boto3 client
        client = boto3.client('rds')
        # delete parameter groups
        for parameter_group in parameter_groups:
            client.delete_db_parameter_group(DBParameterGroupName=parameter_group)
        # return successfully code, if done.
        return True
    except Exception as error:
        print(error)
        exit(1)

def delete_cluster_parameter_groups(cluster_parameter_groups: list) -> bool:
    try:
        # init boto3 client
        client = boto3.client('rds')
        # delete cluster parameter groups
        for cluster_parameter_group in cluster_parameter_groups:
            client.delete_db_cluster_parameter_group(
                DBClusterParameterGroupName=cluster_parameter_group)
        # return successfully code, if done.
        return True
    except Exception as error:
        print(error)
        exit(1)

class RDSResources:

    @classmethod
    async def init(cls):
        self = cls()
        self.db_instances = list_db_instances()
        self.db_clusters = list_db_clusters()
        self.subnet_groups = list_subnet_groups()
        self.parameter_groups = list_parameter_groups()
        self.cluster_parameter_groups = list_cluster_parameter_groups()
        return self

    def print(self):
        print("==== RDS DB Instances ====")
        pprint(self.db_instances)
        print("==== RDS DB Clusters ====")
        pprint(self.db_clusters)
        print("==== RDS Subnet Groups ====")
        pprint(self.subnet_groups)
        print("==== RDS Parameter Groups ====")
        pprint(self.parameter_groups)
        print("==== RDS Cluster Parameter Groups ====")
        pprint(self.cluster_parameter_groups)

    def delete(self):
        delete_db_instances(self.db_instances)
        self.db_instances = []
        delete_db_clusters(self.db_clusters)
        self.db_clusters = []
        delete_subnet_groups(self.subnet_groups)
        self.subnet_groups = []
        delete_parameter_groups(self.parameter_groups)
        self.parameter_groups = []
        delete_cluster_parameter_groups(self.cluster_parameter_groups)
        self.cluster_parameter_groups = []