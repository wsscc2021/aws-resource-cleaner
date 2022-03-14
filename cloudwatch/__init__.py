from pprint import pprint
from signal import alarm
import boto3

def list_alarm_names() -> list:
    try:
        client = boto3.client('cloudwatch')
        response = client.describe_alarms()
        return [
            alarm['AlarmName']
            for alarms in response
            for alarm in alarms
        ]
    except Exception as error:
        print(error)
        exit(1)

def delete_alarms(alarm_names: list) -> bool:
    try:
        client = boto3.client('cloudwatch')
        client.delete_alarms(AlarmNames=alarm_names)
        return True
    except Exception as error:
        print(error)
        exit(1)

class CloudwatchResources:
    
    @classmethod
    async def init(cls):
        self = cls()
        self.alarm_names = list_alarm_names()
        return self
    
    def print(self):
        print("==== Cloudwatch Alarms ====")
        pprint(self.alarm_names)
    
    def delete(self):
        if self.alarm_names:
            delete_alarms(self.alarm_names)
            self.alarm_names = []