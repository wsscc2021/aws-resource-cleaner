from pprint import pprint
import boto3

def list_non_attachment_custom_policy_arns() -> list:
    try:
        # init boto3 client
        client = boto3.client('iam')
        # list policies which only custom managed
        response = client.list_policies(
            Scope='Local', # AWS - AWS Managed polices, Local - Custom Managed policies
            OnlyAttached=False,
            PathPrefix='/',
            PolicyUsageFilter='PermissionsPolicy')
        # parse custom policy ARN from above response
        policy_arns = [ policy['Arn'] for policy in response['Policies'] ]
        # pick up only non-attachment custom policy from above policy_arns
        non_attachment_custom_policiy_arns = list()
        for policy_arn in policy_arns:
            response = client.get_policy(PolicyArn=policy_arn)
            if response['Policy']['AttachmentCount'] == 0:
                non_attachment_custom_policiy_arns.append(policy_arn)
        # return
        return non_attachment_custom_policiy_arns
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
        non_attachment_custom_policy_arns = list_non_attachment_custom_policy_arns()
        open_id_connect_provider_arns = list_open_id_connect_provider_arns()
        saml_provider_arns = list_saml_provider_arns()
        print("==== IAM policies (Non-attachment) ====")
        pprint(non_attachment_custom_policy_arns)
        print("==== IAM OIDC providers ====")
        pprint(open_id_connect_provider_arns)
        print("==== IAM SAML providers ====")
        pprint(saml_provider_arns)
        while True:
            confirm = input("Are you sure you want to delete (y/n)? ")
            if confirm == "y":
                delete_policies(non_attachment_custom_policy_arns)
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
