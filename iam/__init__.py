from pprint import pprint
import boto3

def list_custom_policy_arns() -> list:
    try:
        # init boto3 client
        client = boto3.client('iam')
        # list policies which only custom managed
        response = client.list_policies(
            Scope='Local', # AWS - AWS Managed polices, Local - Custom Managed policies
            OnlyAttached=False,
            PathPrefix='/',
            PolicyUsageFilter='PermissionsPolicy')
        # parse ARN from above result that is custom managed policies
        # return ARNs
        return [ policy['Arn'] for policy in response['Policies'] ]
    except Exception as error:
        print(error)
        exit(1)

def delete_policies(policy_arns: list) -> bool:
    try:
        # init boto3 client
        client = boto3.client('iam')
        # delete policies
        for policy_arn in policy_arns:
            client.delete_policy(PolicyArn=policy_arn)
        # return Successfully code(True), if it's done that deleted all policies
        return True
    except Exception as error:
        print(error)
        exit(1)

def list_custom_role_names() -> list:
    try:
        # init boto3 client
        client = boto3.client('iam')
        # list all roles in account
        response = client.list_roles(PathPrefix='/')
        all_role_names = [ role['RoleName'] for role in response['Roles'] ]
        # list roles which only using at aws-service
        response = client.list_roles(PathPrefix='/aws-service-role/')
        service_role_names = [ role['RoleName'] for role in response['Roles'] ]
        # custom_role_names is all except '/aws-service-role/' roles
        custom_role_names = list(set(all_role_names) - set(service_role_names))
        # return custom roles
        return custom_role_names
    except Exception as error:
        print(error)
        exit(1)

def delete_roles(role_names: list) -> bool:
    try:
        # init boto3 client
        client = boto3.client('iam')
        # delete roles
        for role_name in role_names:
            client.delete_role(RoleName=role_name)
        # return Successfully code(True), if it's done that deleted all roles
        return True
    except Exception as error:
        print(error)
        exit(1)

def list_group_names() -> list:
    try:
        # init boto3 client
        client = boto3.client('iam')
        # list all groups
        response = client.list_groups(PathPrefix='/')
        # parse GroupName from above result
        # return GroupNames
        return [ group['GroupName'] for group in response['Groups'] ]
    except Exception as error:
        print(error)
        exit(1)

def delete_groups(group_names: list) -> bool:
    try:
        # init boto3 client
        client = boto3.client('iam')
        # delete groups
        for group_name in group_names:
            client.delete_group(GroupName=group_name)
        # return Successfully code(True), if it's done that deleted all groups
        return True
    except Exception as error:
        print(error)
        exit(1)

def list_user_names() -> list:
    try:
        # init boto3 client
        client = boto3.client('iam')
        # list all users
        response = client.list_users(PathPrefix='/')
        # parse UserName from above result
        # return UserNames
        return [ user['UserName'] for user in response['Users'] ]
    except Exception as error:
        print(error)
        exit(1)

def delete_users(user_names: list) -> bool:
    try:
        # init boto3 client
        client = boto3.client('iam')
        # delete users
        for user_name in user_names:
            client.delete_user(UserName=user_name)
        # return Successfully code(True), if it's done that deleted all users
        return True
    except Exception as error:
        print(error)
        exit(1)

def list_open_id_connect_provider_arns() -> list:
    try:
        # init boto3 client
        client = boto3.client('iam')
        # list all oidc provider
        response = client.list_open_id_connect_providers()
        # parse Arn from above result
        # return Arn
        return [ oidc['Arn'] for oidc in response['OpenIDConnectProviderList'] ]
    except Exception as error:
        print(error)
        exit(1)

def delete_open_id_connect_providers(open_id_connect_provider_arns: list) -> bool:
    try:
        # init boto3 client
        client = boto3.client('iam')
        # delete users
        for open_id_connect_provider_arn in open_id_connect_provider_arns:
            client.delete_open_id_connect_provider(
                OpenIDConnectProviderArn=open_id_connect_provider_arn)
        # return Successfully code(True), if it's done that deleted all saml_provider_arn
        return True
    except Exception as error:
        print(error)
        exit(1)

def list_saml_provider_arns() -> list:
    try:
        # init boto3 client
        client = boto3.client('iam')
        # list all oidc provider
        response = client.list_saml_providers()
        # parse Arn from above result
        # return Arn
        return [ saml['Arn'] for saml in response['SAMLProviderList'] ]
    except Exception as error:
        print(error)
        exit(1)

def delete_saml_providers(saml_provider_arns: list) -> bool:
    try:
        # init boto3 client
        client = boto3.client('iam')
        # delete users
        for saml_provider_arn in saml_provider_arns:
            client.delete_saml_provider(SAMLProviderArn=saml_provider_arn)
        # return Successfully code(True), if it's done that deleted all saml_provider_arn
        return True
    except Exception as error:
        print(error)
        exit(1)

def iam_cleaner() -> bool:
    try:
        custom_policy_arns = list_custom_policy_arns()
        custom_role_names = list_custom_role_names()
        group_names = list_group_names()
        user_names = list_user_names()
        open_id_connect_provider_arns = list_open_id_connect_provider_arns()
        saml_provider_arns = list_saml_provider_arns()
        print("==== IAM groups ====")
        pprint(group_names)
        print("==== IAM users ====")
        pprint(user_names)
        print("==== IAM roles ====")
        pprint(custom_role_names)
        print("==== IAM policies ====")
        pprint(custom_policy_arns)
        print("==== IAM OIDC providers ====")
        pprint(open_id_connect_provider_arns)
        print("==== IAM SAML providers ====")
        pprint(saml_provider_arns)
        while True:
            confirm = input("Are you sure you want to delete (y/n)? ")
            if confirm == "y":
                delete_groups(group_names)
                delete_users(user_names)
                delete_roles(custom_role_names)
                delete_policies(custom_policy_arns)
                delete_open_id_connect_providers(open_id_connect_provider_arns)
                delete_saml_providers(saml_provider_arns)
                return True
            elif confirm == "n":
                print("Canceled")
                exit(1)
            else:
                print("Only input 'y' or 'n', Try again! ")
    except Exception as error:
        print(error)
        exit(1)

if __name__ == '__main__':
    result = iam_cleaner()
    if result:
        print("done!")
