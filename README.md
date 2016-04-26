# Stelligent Mini Project - Automation for the People

This python project will deploy an EC2 instance on AWS running AWS linux, Apache Web Server and a static page to display "Automation for the People"

## Requirements
- AWS account with CloudFormation and EC2 enabled with IAM credentials.
- AWS credentials file or AWS environment variables `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`
- Python >= 2.7 with boto3, time, requests and argparse modules
- AWS EC2 keypair 

## Installation
Download the Mini Project:
```sh
git clone https://github.com/jason-tasker/stelligent-mini-project
```

## Execution
Deploy 
```sh
cd stelligent-mini-project
python mini_project.py -k <EC2 registered SSH Key Pair>
```

## Usage
```text
usage: mini_project2.py [-h] [--profile PROFILE] [--keyfile KEYFILE]
                        [--ec2instance EC2INSTANCE] [--template TEMPLATE]
                        [--stack-name STACKNAME] [--command COMMAND]
                        [--access-ssh ACCESSSSH]

optional arguments:

  -h, --help            
                        show this help message and exit

  --profile PROFILE, -p PROFILE
                        AWS profile to use in credentials file
  --keyfile KEYFILE, -k KEYFILE
                        EC2 keyfile for SSH management of instance
  --ec2instance EC2INSTANCE, -e EC2INSTANCE
                        EC2 instance size
  --template TEMPLATE, -t TEMPLATE
                        Cloudformation template file in JSON format
  --stack-name STACKNAME, -s STACKNAME
                        Cloudformation Stackname
  --command COMMAND, -c COMMAND
                        install - create stack, delete - delete stack
  --access-ssh ACCESSSSH, -a ACCESSSSH
                        CIDR IP address for SSH access
                        
```
