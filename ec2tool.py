from phi.tools import Toolkit

try:
    import boto3
except ImportError:
    raise ImportError("boto3 is required for EC2Tool. Please install it using `pip install boto3`.")

class EC2Tool(Toolkit):
    name: str = "EC2Tool"
    description: str = "A tool for interacting with AWS EC2 instances"

    def __init__(self, region_name: str = "us-east-1"):
        super().__init__()
        self.client = boto3.client("ec2", region_name=region_name)
        self.register(self.list_instances)
        self.register(self.start_instance)
        self.register(self.stop_instance)

    def list_instances(self) -> str:
        try:
            response = self.client.describe_instances()
            instances = []
            for reservation in response["Reservations"]:
                for instance in reservation["Instances"]:
                    instances.append(instance["InstanceId"])
            return f"Available EC2 instances: {', '.join(instances)}"
        except Exception as e:
            return f"Error listing instances: {str(e)}"

    def start_instance(self, instance_id: str) -> str:
        try:
            self.client.start_instances(InstanceIds=[instance_id])
            return f"Instance started successfully: {instance_id}"
        except Exception as e:
            return f"Error starting instance: {str(e)}"

    def stop_instance(self, instance_id: str) -> str:
        try:
            self.client.stop_instances(InstanceIds=[instance_id])
            return f"Instance stopped successfully: {instance_id}"
        except Exception as e:
            return f"Error stopping instance: {str(e)}"