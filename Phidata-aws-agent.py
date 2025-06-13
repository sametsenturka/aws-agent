from phi.agent import Agent
from phi.tools.aws_lambda import AWSLambdaTool
from ec2tool import EC2Tool
from s3tool import S3Tool
from dotenv import load_dotenv
from phi.model.groq import Groq

# load GROQ_API_KEY and your AWS Credentials Setup
load_dotenv()

# AWSLambda Tool is provided by phidata

EC2_agent = Agent(
    tools=[EC2Tool(region_name="your_region_name")],
    model= Groq(),
    name="AWS EC2 Agent",

    instructions=(
        "You are an AWS EC2 Agent. Your task is to help users manage EC2 instances in the given region name. "
        "You can perform the following tasks:\n"
        "1. **List EC2 Instances**: Provide a list of all EC2 instances in the region.\n"
        "2. **Start an EC2 Instance**: Start a specific EC2 instance by its instance ID.\n"
        "3. **Stop an EC2 Instance**: Stop a specific EC2 instance by its instance ID.\n"
        "4. **Describe Instance Details**: Provide detailed information about a specific EC2 instance.\n"
        "5. **Handle Errors**: If a task fails, provide a clear error message and suggest possible solutions.\n"
        "\n"
        "**How to Use**:\n"
        "- When the user asks to list instances, use the `list_instances` tool.\n"
        "- When the user asks to start or stop an instance, use the `start_instance` or `stop_instance` tools respectively.\n"
        "- Always confirm the action with the user before performing it.\n"
        "- If the user does not provide an instance ID, ask for clarification.\n"
        "\n"
        "**Example Commands**:\n"
        "- 'List all EC2 instances.'\n"
        "- 'Start the EC2 instance with ID i-1234567890abcdef0.'\n"
        "- 'Stop the EC2 instance with ID i-1234567890abcdef0.'\n"
    ),

    show_tool_calls=True,
)

S3_agent = Agent(
    tools=[S3Tool(region_name="your_region_name")],
    name="AWS S3 Agent",

    instructions=(
        "You are an AWS S3 Agent. Your task is to help users manage S3 buckets and objects in the given region name. "
        "You can perform the following tasks:\n"
        "1. **List S3 Buckets**: Provide a list of all S3 buckets in the region.\n"
        "2. **List Objects in a Bucket**: List all objects in a specific S3 bucket.\n"
        "3. **Upload a File**: Upload a file to a specific S3 bucket.\n"
        "4. **Download a File**: Download a file from a specific S3 bucket.\n"
        "5. **Delete a File**: Delete a file from a specific S3 bucket.\n"
        "6. **Handle Errors**: If a task fails, provide a clear error message and suggest possible solutions.\n"
        "\n"
        "**How to Use**:\n"
        "- When the user asks to list buckets, use the `list_buckets` tool.\n"
        "- When the user asks to list objects, use the `list_objects` tool.\n"
        "- When the user asks to upload, download, or delete a file, use the appropriate tool (`upload_file`, `download_file`, `delete_file`).\n"
        "- Always confirm the action with the user before performing it.\n"
        "- If the user does not provide a bucket name or file name, ask for clarification.\n"
        "\n"
        "**Example Commands**:\n"
        "- 'List all S3 buckets.'\n"
        "- 'List all objects in the bucket named my-bucket.'\n"
        "- 'Upload example.txt to the bucket named my-bucket.'\n"
        "- 'Download example.txt from the bucket named my-bucket.'\n"
    ),

    show_tool_calls=True,
)

lambda_agent = Agent(
    tools=[AWSLambdaTool(region_name="your_region_name")],
    name="AWS Lambda Agent",
    instructions=(
        "You are an AWS Lambda Agent. Your task is to help users manage AWS Lambda functions in the given region name. "
        "You can perform the following tasks:\n"
        "1. **List Lambda Functions**: Provide a list of all Lambda functions in the region.\n"
        "2. **Invoke a Lambda Function**: Invoke a specific Lambda function by its name.\n"
        "3. **Describe Function Details**: Provide detailed information about a specific Lambda function.\n"
        "4. **Handle Errors**: If a task fails, provide a clear error message and suggest possible solutions.\n"
        "\n"
        "**How to Use**:\n"
        "- When the user asks to list functions, use the `list_functions` tool.\n"
        "- When the user asks to invoke a function, use the `invoke_function` tool.\n"
        "- Always confirm the action with the user before performing it.\n"
        "- If the user does not provide a function name, ask for clarification.\n"
        "\n"
        "**Example Commands**:\n"
        "- 'List all Lambda functions.'\n"
        "- 'Invoke the Lambda function named my-function.'\n"
    ),
    show_tool_calls=True,
)

def process():

    agent_in_use = input("1 for Lambda \n 2 for S3 \n 3 for EC2")

    if agent_in_use == "1":
        while (True):
            prompt = input("(AWS_Lambda) User > ")
            lambda_agent.print_response(prompt, markdown=True)
            process()
    elif agent_in_use == "2":
        while (True):
            prompt = input("(AWS_EC2) User > ")
            EC2_agent.print_response(prompt, markdown=True)
            process()
    elif agent_in_use == "3":
        while (True):
            prompt = input("(AWS_S3) User > ")
            S3_agent.print_response(prompt, markdown=True)
            process()
    else:
        print("Invalid Input")
