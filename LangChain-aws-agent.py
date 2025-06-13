import os
import boto3
from typing import List, Dict, Any, Optional
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.tools import BaseTool
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_core.tools import ToolException
from pydantic import BaseModel, Field
import json
from datetime import datetime

from dotenv import load_dotenv
load_dotenv()

class EC2ListInstancesInput(BaseModel):
    """Input for EC2 list instances tool."""
    filters: Optional[Dict[str, List[str]]] = Field(
        default=None, 
        description="Optional filters for EC2 instances (e.g., {'instance-state-name': ['running']})"
    )

class EC2StartInstanceInput(BaseModel):
    """Input for EC2 start instance tool."""
    instance_id: str = Field(description="The ID of the EC2 instance to start")

class EC2StopInstanceInput(BaseModel):
    """Input for EC2 stop instance tool."""
    instance_id: str = Field(description="The ID of the EC2 instance to stop")

class S3ListBucketsInput(BaseModel):
    """Input for S3 list buckets tool."""
    pass

class S3UploadFileInput(BaseModel):
    """Input for S3 upload file tool."""
    file_path: str = Field(description="Local path to the file to upload")
    bucket_name: str = Field(description="Name of the S3 bucket")
    key: Optional[str] = Field(default=None, description="S3 key (path) for the file. If not provided, uses filename")

class S3DownloadFileInput(BaseModel):
    """Input for S3 download file tool."""
    bucket_name: str = Field(description="Name of the S3 bucket")
    key: str = Field(description="S3 key (path) of the file to download")
    local_path: str = Field(description="Local path where to save the downloaded file")

class LambdaListFunctionsInput(BaseModel):
    """Input for Lambda list functions tool."""
    pass

class LambdaInvokeFunctionInput(BaseModel):
    """Input for Lambda invoke function tool."""
    function_name: str = Field(description="Name of the Lambda function to invoke")
    payload: Optional[Dict[str, Any]] = Field(default=None, description="Payload to send to the function")

class EC2ListInstancesTool(BaseTool):
    name: str = "ec2_list_instances"
    description: str = "List all EC2 instances with their details including ID, state, type, and tags"
    args_schema = EC2ListInstancesInput
    
    def __init__(self, region_name: str = "us-east-1"):
        super().__init__()
        self.ec2 = boto3.client('ec2', region_name=region_name)
    
    def _run(self, filters: Optional[Dict[str, List[str]]] = None) -> str:
        try:
            kwargs = {}
            if filters:
                kwargs['Filters'] = [{'Name': k, 'Values': v} for k, v in filters.items()]
            
            response = self.ec2.describe_instances(**kwargs)
            
            instances = []
            for reservation in response['Reservations']:
                for instance in reservation['Instances']:
                    instance_info = {
                        'InstanceId': instance['InstanceId'],
                        'State': instance['State']['Name'],
                        'InstanceType': instance['InstanceType'],
                        'LaunchTime': instance['LaunchTime'].strftime('%Y-%m-%d %H:%M:%S'),
                        'Tags': {tag['Key']: tag['Value'] for tag in instance.get('Tags', [])}
                    }
                    instances.append(instance_info)
            
            return json.dumps(instances, indent=2, default=str)
        except Exception as e:
            raise ToolException(f"Error listing EC2 instances: {str(e)}")

class EC2StartInstanceTool(BaseTool):
    name: str = "ec2_start_instance"
    description: str = "Start an EC2 instance by its instance ID"
    args_schema = EC2StartInstanceInput
    
    def __init__(self, region_name: str = "us-east-1"):
        super().__init__()
        self.ec2 = boto3.client('ec2', region_name=region_name)
    
    def _run(self, instance_id: str) -> str:
        try:
            response = self.ec2.start_instances(InstanceIds=[instance_id])
            return f"Starting instance {instance_id}. Current state: {response['StartingInstances'][0]['CurrentState']['Name']}"
        except Exception as e:
            raise ToolException(f"Error starting EC2 instance {instance_id}: {str(e)}")

class EC2StopInstanceTool(BaseTool):
    name: str = "ec2_stop_instance"
    description: str = "Stop an EC2 instance by its instance ID"
    args_schema = EC2StopInstanceInput
    
    def __init__(self, region_name: str = "us-east-1"):
        super().__init__()
        self.ec2 = boto3.client('ec2', region_name=region_name)
    
    def _run(self, instance_id: str) -> str:
        try:
            response = self.ec2.stop_instances(InstanceIds=[instance_id])
            return f"Stopping instance {instance_id}. Current state: {response['StoppingInstances'][0]['CurrentState']['Name']}"
        except Exception as e:
            raise ToolException(f"Error stopping EC2 instance {instance_id}: {str(e)}")

class S3ListBucketsTool(BaseTool):
    name: str = "s3_list_buckets"
    description: str = "List all S3 buckets in your AWS account"
    args_schema = S3ListBucketsInput
    
    def __init__(self, region_name: str = "us-east-1"):
        super().__init__()
        self.s3 = boto3.client('s3', region_name=region_name)
    
    def _run(self) -> str:
        try:
            response = self.s3.list_buckets()
            buckets = []
            for bucket in response['Buckets']:
                bucket_info = {
                    'Name': bucket['Name'],
                    'CreationDate': bucket['CreationDate'].strftime('%Y-%m-%d %H:%M:%S')
                }
                buckets.append(bucket_info)
            
            return json.dumps(buckets, indent=2)
        except Exception as e:
            raise ToolException(f"Error listing S3 buckets: {str(e)}")

class S3UploadFileTool(BaseTool):
    name: str = "s3_upload_file"
    description: str = "Upload a file to an S3 bucket"
    args_schema = S3UploadFileInput
    
    def __init__(self, region_name: str = "us-east-1"):
        super().__init__()
        self.s3 = boto3.client('s3', region_name=region_name)
    
    def _run(self, file_path: str, bucket_name: str, key: Optional[str] = None) -> str:
        try:
            if not key:
                key = os.path.basename(file_path)
            
            self.s3.upload_file(file_path, bucket_name, key)
            return f"Successfully uploaded {file_path} to s3://{bucket_name}/{key}"
        except Exception as e:
            raise ToolException(f"Error uploading file to S3: {str(e)}")

class S3DownloadFileTool(BaseTool):
    name: str = "s3_download_file"
    description: str = "Download a file from an S3 bucket"
    args_schema = S3DownloadFileInput
    
    def __init__(self, region_name: str = "us-east-1"):
        super().__init__()
        self.s3 = boto3.client('s3', region_name=region_name)
    
    def _run(self, bucket_name: str, key: str, local_path: str) -> str:
        try:
            self.s3.download_file(bucket_name, key, local_path)
            return f"Successfully downloaded s3://{bucket_name}/{key} to {local_path}"
        except Exception as e:
            raise ToolException(f"Error downloading file from S3: {str(e)}")

class LambdaListFunctionsTool(BaseTool):
    name: str = "lambda_list_functions"
    description: str = "List all Lambda functions in your AWS account"
    args_schema = LambdaListFunctionsInput
    
    def __init__(self, region_name: str = "us-east-1"):
        super().__init__()
        self.lambda_client = boto3.client('lambda', region_name=region_name)
    
    def _run(self) -> str:
        try:
            response = self.lambda_client.list_functions()
            functions = []
            for func in response['Functions']:
                func_info = {
                    'FunctionName': func['FunctionName'],
                    'Runtime': func['Runtime'],
                    'Handler': func['Handler'],
                    'LastModified': func['LastModified'],
                    'Description': func.get('Description', 'No description')
                }
                functions.append(func_info)
            
            return json.dumps(functions, indent=2)
        except Exception as e:
            raise ToolException(f"Error listing Lambda functions: {str(e)}")

class LambdaInvokeFunctionTool(BaseTool):
    name: str = "lambda_invoke_function"
    description: str = "Invoke a Lambda function with optional payload"
    args_schema = LambdaInvokeFunctionInput
    
    def __init__(self, region_name: str = "us-east-1"):
        super().__init__()
        self.lambda_client = boto3.client('lambda', region_name=region_name)
    
    def _run(self, function_name: str, payload: Optional[Dict[str, Any]] = None) -> str:
        try:
            kwargs = {'FunctionName': function_name}
            if payload:
                kwargs['Payload'] = json.dumps(payload)
            
            response = self.lambda_client.invoke(**kwargs)
            
            result = {
                'StatusCode': response['StatusCode'],
                'ExecutedVersion': response['ExecutedVersion']
            }
            
            if 'Payload' in response:
                payload_content = response['Payload'].read().decode('utf-8')
                result['Payload'] = json.loads(payload_content) if payload_content else None
            
            return json.dumps(result, indent=2)
        except Exception as e:
            raise ToolException(f"Error invoking Lambda function {function_name}: {str(e)}")

class AWSAgent:
    def __init__(self, region_name: str = "us-east-1", model_name: str = "llama-3.3-70b-versatile"):
        self.region_name = region_name
        
        self.llm = ChatGroq(
            model=model_name,
            temperature=0,
            api_key=os.getenv("GROQ_API_KEY")
        )
        
        self.ec2_tools = [
            EC2ListInstancesTool(region_name),
            EC2StartInstanceTool(region_name),
            EC2StopInstanceTool(region_name)
        ]
        
        self.s3_tools = [
            S3ListBucketsTool(region_name),
            S3UploadFileTool(region_name),
            S3DownloadFileTool(region_name)
        ]
        
        self.lambda_tools = [
            LambdaListFunctionsTool(region_name),
            LambdaInvokeFunctionTool(region_name)
        ]
    
        self.ec2_agent = self._create_agent(
            self.ec2_tools,
            "AWS EC2 Management Agent",
            """You are an AWS EC2 management specialist. You can:
            - List all EC2 instances with their details
            - Start EC2 instances by their instance ID
            - Stop EC2 instances by their instance ID
            
            Always provide clear, helpful responses about EC2 operations.
            When listing instances, format the output clearly.
            Before starting or stopping instances, confirm the instance ID exists."""
        )
        
        self.s3_agent = self._create_agent(
            self.s3_tools,
            "AWS S3 Management Agent",
            """You are an AWS S3 management specialist. You can:
            - List all S3 buckets in the account
            - Upload files to S3 buckets
            - Download files from S3 buckets
            
            Always provide clear feedback about S3 operations.
            When uploading or downloading files, confirm the operation was successful.
            Be helpful with S3 bucket and key naming conventions."""
        )
        
        self.lambda_agent = self._create_agent(
            self.lambda_tools,
            "AWS Lambda Management Agent",
            """You are an AWS Lambda management specialist. You can:
            - List all Lambda functions in the account
            - Invoke Lambda functions with or without payload
            
            Always provide clear information about Lambda operations.
            When invoking functions, show the response clearly.
            Help users understand function invocation results."""
        )
        
        all_tools = self.ec2_tools + self.s3_tools + self.lambda_tools
        self.unified_agent = self._create_agent(
            all_tools,
            "AWS Multi-Service Agent",
            """You are a comprehensive AWS management agent. You can manage:
            
            EC2 Services:
            - List, start and stop EC2 instances
            
            S3 Services:
            - List buckets, upload and download files
            
            Lambda Services:
            - List and invoke Lambda functions
            
            Always determine which AWS service the user wants to work with and use the appropriate tools.
            Provide clear, helpful responses and confirm operations when completed.
            If you're unsure about what service to use, ask for clarification."""
        )
    
    def _create_agent(self, tools: List[BaseTool], name: str, instructions: str) -> AgentExecutor:
        prompt = ChatPromptTemplate.from_messages([
            ("system", f"{instructions}\n\nYou have access to the following tools: {[tool.name for tool in tools]}"),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ])
        
        agent = create_tool_calling_agent(self.llm, tools, prompt)
        return AgentExecutor(agent=agent, tools=tools, verbose=True)
    
    def execute_ec2_command(self, command: str) -> str:
        """Execute EC2-specific commands"""
        return self.ec2_agent.invoke({"input": command})["output"]
    
    def execute_s3_command(self, command: str) -> str:
        """Execute S3-specific commands"""
        return self.s3_agent.invoke({"input": command})["output"]
    
    def execute_lambda_command(self, command: str) -> str:
        """Execute Lambda-specific commands"""
        return self.lambda_agent.invoke({"input": command})["output"]
    
    def execute_command(self, command: str) -> str:
        """Execute any AWS command using the unified agent"""
        return self.unified_agent.invoke({"input": command})["output"]


def main():
    agent = AWSAgent(region_name=os.getenv("AWS_REGION", "us-east-1"))
    
    print("AWS Agent with LangChain - Ready!")
    print("=" * 50)
    
    examples = [
        "List all EC2 instances",
        "List all S3 buckets",
        "List all Lambda functions",
        "Start EC2 instance i-1234567890abcdef0",
        "Upload example.txt to my-bucket",
        "Invoke Lambda function my-function"
    ]
    
    print("Example commands you can try:")
    for i, example in enumerate(examples, 1):
        print(f"{i}. {example}")
    
    print("\n" + "=" * 50)
    
    while True:
        try:
            user_input = input("\nEnter your AWS command (or 'quit' to exit): ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            
            if not user_input:
                continue
            
            print(f"\nExecuting: {user_input}")
            print("-" * 30)
            
            result = agent.execute_command(user_input)
            print(result)
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
