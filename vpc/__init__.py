from pprint import pprint
import boto3
import botocore

def list_vpc_ids() -> list:
    try:
        client = boto3.client('ec2')
        response = client.describe_vpcs(
            Filters=[
                {
                    'Name': 'is-default',
                    'Values': [
                        'false',
                    ]
                },
            ],
        )
        return [
            vpc['VpcId']
            for vpc in response['Vpcs']
        ]
    except Exception as error:
        print(error)
        exit(1)

def delete_vpcs(vpc_ids: list) -> bool:
    try:
        client = boto3.client('ec2')
        for vpc_id in vpc_ids:
            client.delete_vpc(VpcId=vpc_id)
        return True
    except Exception as error:
        print(error)
        exit(1)

def list_nat_gateway_ids(vpc_ids: list) -> list:
    try:
        if not vpc_ids: return []
        client = boto3.client('ec2')
        response = client.describe_nat_gateways(
            Filters=[
                {
                    'Name': 'state',
                    'Values': [
                        'pending',
                        'available',
                    ]
                },
                {
                    'Name': 'vpc-id',
                    'Values': vpc_ids
                }
            ]
        )
        return [
            nat_gateway['NatGatewayId']
            for nat_gateway in response['NatGateways']
        ]
    except Exception as error:
        print(error)
        exit(1)

def delete_nat_gateways(nat_gateway_ids: list) -> bool:
    try:
        client = boto3.client('ec2')
        for nat_gateway_id in nat_gateway_ids:
            client.delete_nat_gateway(NatGatewayId=nat_gateway_id)
        waiter = client.get_waiter('nat_gateway_available')
        waiter.wait(
            Filters=[
                {
                    'Name': 'state',
                    'Values': [
                        'deleted',
                    ]
                },
                {
                    'Name': 'nat-gateway-id',
                    'Values': nat_gateway_ids
                }
            ],
        )
        return True
    except botocore.exceptions.WaiterError as error:
        # please attention the issue: https://github.com/aws/aws-sdk/issues/61
        if error.kwargs['name'] == 'NatGatewayAvailable' and error.kwargs['reason'] == 'Waiter encountered a terminal failure state: For expression "NatGateways[].State" we matched expected path: "deleted" at least once':
            return True
        else:
            raise Exception(error)
    except Exception as error:
        print(error)
        exit(1)

def list_vpc_endpoint_ids(vpc_ids: list) -> list:
    try:
        if not vpc_ids: return []
        client = boto3.client('ec2')
        response = client.describe_vpc_endpoints(
            Filters=[
                {
                    'Name': 'vpc-id',
                    'Values': vpc_ids
                },
            ],
        )
        return [
            endpoint['VpcEndpointId']
            for endpoint in response['VpcEndpoints']
        ]
    except Exception as error:
        print(error)
        exit(1)

def delete_vpc_endpoints(vpc_endpoint_ids: list) -> bool:
    try:
        client = boto3.client('ec2')
        client.delete_vpc_endpoints(VpcEndpointIds=vpc_endpoint_ids)
        return True
    except Exception as error:
        print(error)
        exit(1)

def list_vpc_peering_connection_ids(vpc_ids: list) -> list:
    try:
        if not vpc_ids: return []
        client = boto3.client('ec2')
        status_filter = {
            'Name': 'status-code',
            'Values': ['pending-acceptance','expired','provisioning','active','rejected']
        }
        accepter_filter = {
            'Name': 'accepter-vpc-info.vpc-id',
            'Values': vpc_ids
        }
        requester_filter = {
            'Name': 'requester-vpc-info.vpc-id',
            'Values': vpc_ids
        }
        response = client.describe_vpc_peering_connections(
            Filters=[ status_filter, accepter_filter ],
        )
        vpc_peering_connection_ids = [
            vpc_peering_connection['VpcPeeringConnectionId']
            for vpc_peering_connection in response['VpcPeeringConnections']
        ]
        response = client.describe_vpc_peering_connections(
            Filters=[ status_filter, requester_filter ],
        )
        vpc_peering_connection_ids += [
            vpc_peering_connection['VpcPeeringConnectionId']
            for vpc_peering_connection in response['VpcPeeringConnections']
        ]
        return vpc_peering_connection_ids
    except Exception as error:
        print(error)
        exit(1)

def delete_vpc_peering_connections(vpc_peering_connection_ids: list) -> bool:
    try:
        client = boto3.client('ec2')
        for vpc_peering_connection_id in vpc_peering_connection_ids:
            client.delete_vpc_peering_connection(
                VpcPeeringConnectionId=vpc_peering_connection_id)
        waiter = client.get_waiter('vpc_peering_connection_deleted')
        waiter.wait(VpcPeeringConnectionIds=vpc_peering_connection_ids)
        return True
    except Exception as error:
        print(error)
        exit(1)

def list_vpc_subnet_ids(vpc_ids: list) -> bool:
    try:
        if not vpc_ids: return []
        client = boto3.client('ec2')
        response = client.describe_subnets(
            Filters=[
                {
                    'Name': 'vpc-id',
                    'Values': vpc_ids
                },
            ]
        )
        return [
            subnet['SubnetId']
            for subnet in response['Subnets']
        ]
    except Exception as error:
        print(error)
        exit(1)

def delete_vpc_subnets(subnet_ids: list) -> bool:
    try:
        client = boto3.client('ec2')
        for subnet_id in subnet_ids:
            client.delete_subnet(SubnetId=subnet_id)
        return True
    except Exception as error:
        print(error)
        exit(1)

def delete_internet_gateways(vpc_ids: list) -> bool:
    try:
        if not vpc_ids: return []
        client = boto3.client('ec2')
        response = client.describe_internet_gateways(
            Filters=[
                {
                    'Name': 'attachment.vpc-id',
                    'Values': vpc_ids
                },
            ],
        )
        for internet_gateway in response['InternetGateways']:
            for attachment in internet_gateway['Attachments']:
                client.detach_internet_gateway(
                    InternetGatewayId=internet_gateway['InternetGatewayId'],
                    VpcId=attachment['VpcId'])
            client.delete_internet_gateway(
                InternetGatewayId=internet_gateway['InternetGatewayId'])
        return True
    except Exception as error:
        print(error)
        exit(1)

def delete_route_tables(vpc_ids: list) -> bool:
    try:
        if not vpc_ids: return []
        client = boto3.client('ec2')
        response = client.describe_route_tables(
            Filters=[
                {
                    'Name': 'vpc-id',
                    'Values': vpc_ids
                },
            ],
        )
        for route_table in response['RouteTables']:
            if route_table['Associations'] and route_table['Associations'][0]['Main']: continue
            for route in route_table['Routes']:
                if 'GatewayId' in route and route['GatewayId'] == 'local': continue
                client.delete_route(
                    DestinationCidrBlock=route['DestinationCidrBlock'],
                    RouteTableId=route_table['RouteTableId'])
            client.delete_route_table(RouteTableId=route_table['RouteTableId'])
        return True
    except Exception as error:
        print(error)
        exit(1)

class VpcResources:

    def __init__(self):
        self.vpc_ids                    = list_vpc_ids()
        self.nat_gateway_ids            = list_nat_gateway_ids(self.vpc_ids) if self.vpc_ids else []
        self.vpc_endpoint_ids           = list_vpc_endpoint_ids(self.vpc_ids) if self.vpc_ids else []
        self.vpc_peering_connection_ids = list_vpc_peering_connection_ids(self.vpc_ids) if self.vpc_ids else []
        self.vpc_subnet_ids             = list_vpc_subnet_ids(self.vpc_ids) if self.vpc_ids else []
    
    def print(self):
        # output will deleted resources list
        print("==== VPC ====")
        pprint(self.vpc_ids)
        print("==== NAT Gateways ====")
        pprint(self.nat_gateway_ids)
        print("==== VPC Endpoints ====")
        pprint(self.vpc_endpoint_ids)
        print("==== VPC Peering Connections ====")
        pprint(self.vpc_peering_connection_ids)
        print("==== VPC Subnets ====")
        pprint(self.vpc_subnet_ids)

    def delete(self):
        if self.nat_gateway_ids:
            delete_nat_gateways(self.nat_gateway_ids)
            self.nat_gateway_ids = []

        if self.vpc_endpoint_ids:
            delete_vpc_endpoints(self.vpc_endpoint_ids)
            self.vpc_endpoint_ids = []

        if self.vpc_peering_connection_ids:
            delete_vpc_peering_connections(self.vpc_peering_connection_ids)
            self.vpc_peering_connection_ids = []

        if self.vpc_subnet_ids:
            delete_vpc_subnets(self.vpc_subnet_ids)
            self.vpc_subnet_ids = []

        if self.vpc_ids:
            delete_internet_gateways(self.vpc_ids)
            delete_route_tables(self.vpc_ids)
            delete_vpcs(self.vpc_ids)
