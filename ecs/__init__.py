from pprint import pprint
import boto3

def list_task_definitions() -> list:
    try:
        # init boto3 client
        client = boto3.client('ecs')
        # describe all task definitions which status is ACTIVE
        response = client.list_task_definitions(status='ACTIVE')
        # parse and return task definition arns from above response
        return [ task_definition for task_definition in response['taskDefinitionArns'] ]
    except Exception as error:
        print(error)
        exit(1)

def delete_task_definitions(task_definitions: list) -> bool:
    try:
        # init boto3 client
        client = boto3.client('ecs')
        # deregister task definitions
        for task_definition in task_definitions:
            client.deregister_task_definition(taskDefinition=task_definition)
        # return successfully code, if done.
        return True
    except Exception as error:
        print(error)
        exit(1)

def ecs_cleaner() -> bool:
    try:
        # list up all resources at rds service
        task_definitions = list_task_definitions()
        
        # output will deleted resources list
        print("==== ECS Task Definitions ====")
        pprint(task_definitions)

        # approval and delete all resources
        while True:
            confirm = input("Are you sure you want to delete (y/n)? ")
            if confirm == "y":
                delete_task_definitions(task_definitions)
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
    result = ecs_cleaner()
    if result:
        print("done!")