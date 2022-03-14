from pprint import pprint
import boto3

def list_table_names() -> list:
    try:
        client = boto3.client('dynamodb')
        response = client.list_tables()
        return response['TableNames']
    except Exception as error:
        print(error)
        exit(1)

def delete_tables(table_names: list) -> bool:
    try:
        client = boto3.client('dynamodb')
        for table_name in table_names:
            client.delete_table(TableName=table_name)
        return True
    except Exception as error:
        print(error)
        exit(1)

class DynamoDBResources:

    @classmethod
    async def init(cls):
        self = cls()
        self.table_names = list_table_names()
        return self
    
    def print(self):
        print("==== DynamoDB Tables ====")
        pprint(self.table_names)
    
    def delete(self):
        delete_tables(self.table_names)
        self.table_names = []