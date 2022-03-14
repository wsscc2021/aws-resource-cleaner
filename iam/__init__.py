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
        # return successfully code, if done.
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
        # return successfully code, if done.
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
        # return successfully code, if done.
        return True
    except Exception as error:
        print(error)
        exit(1)


class IAMResources:

    @classmethod
    async def init(cls):
        self = cls()
        self.non_attachment_custom_policy_arns = list_non_attachment_custom_policy_arns()
        self.open_id_connect_provider_arns = list_open_id_connect_provider_arns()
        self.saml_provider_arns = list_saml_provider_arns()
        return self

    def print(self):
        print("==== IAM policies (Non-attachment) ====")
        pprint(self.non_attachment_custom_policy_arns)
        print("==== IAM OIDC providers ====")
        pprint(self.open_id_connect_provider_arns)
        print("==== IAM SAML providers ====")
        pprint(self.saml_provider_arns)

    def delete(self):
        # delete custom policy
        if self.non_attachment_custom_policy_arns:
            delete_policies(self.non_attachment_custom_policy_arns)
            self.non_attachment_custom_policy_arns = []
        # delete oidc provider
        if self.open_id_connect_provider_arns:
            delete_open_id_connect_providers(self.open_id_connect_provider_arns)
            self.open_id_connect_provider_arns = []
        # delete saml provider
        if self.saml_provider_arns:
            delete_saml_providers(self.saml_provider_arns)
            self.saml_provider_arns = []