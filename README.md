```markdown
# AWS Agents with Phidata Framework

AI-powered agents to manage AWS services (EC2, S3, Lambda) using natural language commands.
Built with `phidata` and `boto3`.

I used Groq (llama-3.3-70b-versatile) which provides a Free API Key.

---

## 🚀 Features
- EC2 Management: List, start, and stop EC2 instances.
- S3 Management: List buckets, upload/download files, and manage objects.
- Lambda Management: List and invoke Lambda functions.
- AI Integration: Execute tasks using natural language commands.

---

## 📋 Prerequisites

1. Permissions Required:
     - `AmazonEC2FullAccess` (for EC2)
     - `AmazonS3FullAccess` (for S3)
     - `AWSLambda_FullAccess` (for Lambda)

2. Libraries:
   
   pip install boto3 phidata
   ```

## 🔐 Configuration

### AWS Credentials Setup
#### Option 1: Environment Variables (dotenv)

```bash
# Linux/Mac
export AWS_ACCESS_KEY_ID="AKIAXXXXXXXXXXXXXXXX"
export AWS_SECRET_ACCESS_KEY="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
export AWS_REGION= YOUR REGION
export GROQ_API_KEY = "YOUR_API_KEY"

# Windows (PowerShell)
$env:AWS_ACCESS_KEY_ID="AKIAXXXXXXXXXXXXXXXX"
$env:AWS_SECRET_ACCESS_KEY="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
$env:AWS_REGION= YOUR REGION
$env:GROQ_API_KEY= YOUR_API_KEY
```

#### Option 2: AWS Credentials File
Create or edit `~/.aws/credentials` (Linux/Mac) or `%USERPROFILE%\.aws\credentials` (Windows):
```ini
[default]
aws_access_key_id = AKIAXXXXXXXXXXXXXXXX
aws_secret_access_key = XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
region = YOUR_REGION
```

---

### Imports

```python
from phi.agent import Agent
from phi.tools.aws_lambda import AWSLambdaTool (comes with phidata)
from ec2tool import EC2Tool 
from s3tool import S3Tool 
from phi.model.Groq import Groq
from dotenv import load_dotenv

load_dotenv()

```
## 🛠️ Usage (check official doc for more)

```python
ec2_agent = Agent(
    tools=[EC2Tool(region_name=YOUR_REGION)],
    model=Groq(id="llama-3.3-70b-versatile"),
    name="AWS EC2 Agent",
    instructions="...",  # (I will be posting great Instructions in this repo)
    show_tool_calls=True,
)

s3_agent = Agent(
    tools=[S3Tool(region_name=YOUR_REGION)],
    name="AWS S3 Agent",
    model=Groq(id="llama-3.3-70b-versatile"),
    instructions="...",  # (I will be posting great Instructions in this repo)
    show_tool_calls=True,
)

lambda_agent = Agent(
    tools=[AWSLambdaTool(region_name=YOUR_REGION)],
    model=Groq(id="llama-3.3-70b-versatile"),
    name="AWS Lambda Agent",
    instructions="...",  # (I will be posting great Instructions in this repo)
    show_tool_calls=True,
)
```

---

## 💡 Examples

### EC2 Agent
```python
# List all EC2 instances
ec2_agent.print_response("List all EC2 instances.")

# Start an EC2 instance
ec2_agent.print_response("Start the EC2 instance with ID i-1234567890abcdef0.")
```

### S3 Agent
```python
# List S3 buckets
s3_agent.print_response("List all S3 buckets.")

# Upload a file
s3_agent.print_response("Upload example.txt to the bucket named my-bucket.")
```

### Lambda Agent
```python
# List Lambda functions
lambda_agent.print_response("List all Lambda functions.")

# Invoke a Lambda function
lambda_agent.print_response("Invoke the Lambda function named my-function.")
```

---

## I AM NOT SURE  :(
1. I am unsure about the `AmazonEC2FullAccess`, `AmazonS3FullAccess`, and `AmazonLambdaFullAccess` permissions.
2. Full Access to some of your AWS services may not be a great idea.
3. It's good for listing available things in your account.
4. Idk when I take some advanced courses and keep learning, Some of these can be fixed.
   

- **Phidata Documentation**: [https://phidata.com](https://phidata.com)
- **boto3 Documentation**: [boto3 Docs](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)


**NOTE**: A freshman creates this repository. I believe some great opinions about this repo would lead me to learn & develop more.
```
