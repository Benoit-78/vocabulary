
# ====================
# General
# ====================
aws configure


# ====================
# IAM
# ====================
# Policy


# Roles
aws iam attach-role-policy \
    --role-name vocabulary_read_on_bucket \
    --policy-arn arn:aws:iam::aws:policy/AmazonEC2FullAccess

aws iam list-attached-role-policies \
    --role-name vocabulary_read_on_bucket

# User


# ====================
# EC2
# ====================
# ----------
# Security group
# ----------
aws ec2 create-security-group \
    --group-name vocabulary-sg \
    --description "Allows users to access the application" \
    --vpc-id vpc-0011e2cd73034beb9

grep "GroupId" > conf/security_group.txt

# Keep this on a single line
aws ec2 authorize-security-group-ingress --group-id sg-08ebad99d1b1b98b6 --protocol tcp --port 8080 --cidr 0.0.0.0/0
# Keep this on a single line
aws ec2 authorize-security-group-ingress --group-id sg-08ebad99d1b1b98b6 --protocol tcp --port 22 --cidr 88.161.167.12/32

aws ec2 describe-security-groups \
    --group-ids sg-08ebad99d1b1b98b6


# ----------
# Instance
# ----------
# Create a new policy for the IAM user, and declare the following
{
    "Version": "2012-10-17",
    "Statement":
    [
        {
            "Effect": "Allow",
            "Action": "ec2:CreateKeyPair",
            "Resource": "*"
        }
    ]
}

aws ec2 create-key-pair \
    --key-name voc_ssh_key_1 \
    --query 'KeyMaterial' \
    --output text > voc_ssh_key_1.pem

aws ec2 run-instances \
    --image-id ami-00983e8a26e4c9bd9 \
    --instance-type t2.medium \
    --key-name voc_ssh_key_1 \
    --security-group-ids sg-08ebad99d1b1b98b6 \
    --block-device-mappings '[{"DeviceName":"/dev/sda1","Ebs":{"VolumeSize":20,"VolumeType":"gp2"}}]' \
    --tag-specifications 'ResourceType=instance,Tags=[{Key=vocabulary,Value=compute}]' \
    --iam-instance-profile Name=vocabulary_read_on_bucket \
    --user-data file://bin/user_data.sh

grep InstanceId > conf/instance_id.txt

aws ec2 describe-instances \
    --instance-ids i-01334f73020ce5513 \
    --query "Reservations[0].Instances[0].State.Name"

# Create Internet Gateway
aws ec2 create-internet-gateway

grep InternetGatewayId

# Keep this on a single line
aws ec2 attach-internet-gateway --internet-gateway-id igw-067bdaf3b90f544d8 --vpc-id vpc-0011e2cd73034beb9



# Create an elastic IP
aws ec2 allocate-address \
    --domain vpc

grep PublicIp > conf/public_ip.txt
grep AllocationId > conf/allocation_id.txt

aws ec2 associate-address \
    --allocation-id eipalloc-07c0c9dd56ff7585a \
    --instance-id i-0a76b8efc2f9842e3
# Check the route table, and manually confirm the internet gateway
# Check the Access Control List

# Actions -> Monitor and troubleshoot -> Get system log
# Why does an elastic IP address need an internet gateway, and a standard IP address does not?
# How can I know if my instance is on a private or public network?

# Use '-' in the IP address, not '.'
ssh -i conf/voc_ssh_key_1.pem ubuntu@ec2-15-237-121-125.eu-west-3.compute.amazonaws.com



# ====================
# S3
# ====================
aws s3 sync /home/benoit/Documents/vocabulary s3://vocabulary-benito/vocabulary \
    --exclude ".pytest_cache/*" \
    --exclude ".vscode/*" \
    --exclude "__pycache__/*" \
    --exclude ".git/*" \
    --exclude "bin/aws_commands.sh" \
    --exclude "bin/kubectl_create_secret.sh" \
    --exclude "common/*" \
    --exclude "conf/*" \
    --exclude "data/__pycache__/*" \
    --exclude "divers/*" \
    --exclude "doc/*" \
    --exclude "env/*" \
    --exclude "htmlcov/*" \
    --exclude "logs/*" \
    --exclude "mgmt/*" \
    --exclude "src/data/__pycache__/*" \
    --exclude "tests/*" \
    --exclude ".gitignore" \
    --exclude ".coverage" \
    --exclude "common/secret.yaml" \
    --exclude "cred.json" \
    --exclude "nltk_tries_out.py" \
    --exclude "pylintrc" \
    --exclude "pyvenv.cfg" \
    --exclude "README.md" \
    --exclude "token.txt" \
    --exclude "*.exe" \
    --exclude "*.pyc" \
    --exclude "*.pdf" \
    --exclude "*.txt"

# Delete a folder
aws s3 rm s3://vocabulary-benito/vocabulary/logs \
    --recursive

# Delete a file
aws s3 rm s3://vocabulary-benito/vocabulary/bin/aws_commands.sh

# Download
aws s3 cp s3://vocabulary-benito/vocabulary /home/ubuntu/vocabulary \
    --recursive



# =======================
# Environment
# =======================
export PYTHONPATH=/home/ubuntu/vocabulary/src:$PYTHONPATH
cd vocabulary
python3 -m venv env
source env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

uvicorn src.web_app:app --reload --port 8080 --host 0.0.0.0



# =======================
# End of life
# =======================
aws ec2 terminate-instances \
    --instance-ids <instance-id>

aws ec2 release-address \
    --allocation-id <alloc-id>
