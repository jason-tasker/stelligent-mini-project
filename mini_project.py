#!/usr/bin/python 

import boto3
import time
import requests
import argparse

# Date variable for timestamp
date_str = time.strftime("%Y%m%d")

# Time variable for timestamp
time_str = time.strftime("%H%M%S")

website = ""
client = boto3.client('cloudformation')

def create_stack(args):
	print("Creating stack: " + args.stackname)
	print("This process can take a few minutes to complete")
	with open(args.template, 'r') as f:
		response = client.create_stack(
			StackName = (args.stackname),
			TemplateBody=f.read(),
			Parameters = [
				{
				'ParameterKey': 'KeyName',
				'ParameterValue': args.keyfile,
				'UsePreviousValue': False
				},
				{
				'ParameterKey': 'InstanceType',
				'ParameterValue': args.ec2instance,
				'UsePreviousValue': False
				},
				{
				'ParameterKey': 'SSHLocation',
				'ParameterValue': args.accessssh,
				'UsePreviousValue': False
				}
			]
		)

	#print (response)
	waiter = client.get_waiter('stack_create_complete')
	waiter.wait(StackName=args.stackname)

def display_stack(args):
	response = client.describe_stacks(StackName=args.stackname)
	stacks = response['Stacks']

	for stack in stacks:
        	stack_outputs = stack.get('Outputs')
        	stack_outputs = {d['OutputKey']: d['OutputValue'] for d in stack_outputs}

	global website
	website = "http://" + stack_outputs['PublicDNS']
	print("Stack has completed.")
	print("Instance ID: " + stack_outputs['InstanceId'])
	print("Zone: " + stack_outputs['AZ'])
	print("Public DNS: " + stack_outputs['PublicDNS'])
	print("Public IP: " + stack_outputs['PublicIP'])

	print("")

def check_site():
	print("Checking if web site exists")
	
	site_check = "none"
	
	while site_check == "none":
		try: 
			request = requests.get(url=website)
			site_check="valid"
		except:
			print("Waiting on web site")
			time.sleep(30)
	
	if request.status_code == 200:
		print("Web site exists")
	else:
		print("Web site doesn't exist")
	print("")
	print("You can access the website at " + website)


def delete_stack(args):
	print("Deleting stack: " + args.stackname)
	response = client.delete_stack(StackName = args.stackname)

	waiter = client.get_waiter('stack_delete_complete')
	waiter.wait(StackName=args.stackname)

	print("Stack " + args.stackname + " deleted")

	
if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--profile', '-p', dest='profile', default="default", required=False, help="AWS profile to use in credentials file")
	parser.add_argument('--keyfile', '-k', dest='keyfile', default="default-test1", required=False, help="EC2 keyfile for SSH management of instance")
	parser.add_argument('--ec2instance', '-e', dest='ec2instance', default="t2.micro", required=False, help="EC2 instance size")
	parser.add_argument('--template', '-t', dest='template', default="smp_cloudformation.json", required=False, help="Cloudformation template file in JSON format")
	parser.add_argument('--stack-name', '-s', dest='stackname', default="stelligentminiproject", required=False, help="Cloudformation Stackname")
	parser.add_argument('--command', '-c', dest='command', default="install", required=False, help="install - create stack, delete - delete stack")
	parser.add_argument('--access-ssh', '-a', dest='accessssh', default="0.0.0.0/0", required=False, help="CIDR IP address for SSH access")
	args = parser.parse_args()

if args.command == "install":
	create_stack(args)
	display_stack(args)
	check_site()
elif args.command == "delete":
	delete_stack(args)
else:
	print("invalid command")

