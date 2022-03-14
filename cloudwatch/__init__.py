from pprint import pprint
import boto3

def list_alarm_names() -> list:
    try:
        client = boto3.client('cloudwatch')
        response = client.describe_alarms()
        return [
            alarm['AlarmName']
            for alarm in response['CompositeAlarms']
        ] + [
            alarm['AlarmName']
            for alarm in response['MetricAlarms']
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
    
    def __init__(self):
        self.alarm_names = list_alarm_names()
    
    def print(self):
        print("==== Cloudwatch Alarms ====")
        pprint(self.alarm_names)
    
    def delete(self):
        delete_alarms(self.alarm_names)
        self.alarm_names = []