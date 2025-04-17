# usp_iac

#####################  Instructions   ###################
This repo is used to create AWS resources 

Prerequisites before you create resources (AWS and CLI's):

  1. AWS Account from https://signin.aws.amazon.com/ 
  2. IAM User with AdministratorAccess Policy Attached
  3. Under IAM user > Security Credentials generate Access key to make programmmatic calls from the AWS CLI (Access Key ID and Secret access Key are used later)
  4. Install Gitbash on the local machine
  5. On Gitbash: install [AWS CLI](https://hands-on.cloud/install-aws-cli/)
  6. On Gitbash: install terraform v1.5.6 from https://releases.hashicorp.com/terraform/1.5.6/ 
  
	```bash 
	mkdir -p ~/Desktop/Work/terraform
	cd ~/Desktop/Work/terraform
	curl -LO "https://releases.hashicorp.com/terraform/1.5.6/terraform_1.5.6_windows_amd64.zip"
	mv terraform.exe "~/Desktop/Work/terraform"
	export PATH=$PATH:~/Desktop/Work/terraform
	terraform version
	```
	
  7. On GitBash --> Download the code:
  
	```bash
	$ git clone https://<yourusername>@bitbucket.org/<yourbitbucketrepo>.git -b main
	```
	
  8. On GitBash --> export AWS_ACCESS_KEY_ID & AWS_SECRET_ACCESS_KEY from step 3 above along with the region where the resources created:
  
	```bash
	$ export AWS_ACCESS_KEY_ID=****
	$ export AWS_SECRET_ACCESS_KEY=***
	$ export AWS_DEFAULT_REGION=us-east-1
	$ .automation/deploy.sh -access-key "${AWS_ACCESS_KEY_ID}" -secret-key "${AWS_SECRET_ACCESS_KEY}" -environment <dev OR test OR prod> 
	```
