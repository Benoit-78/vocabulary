
minikube ip

k config set-context --current --namespace=vocabulary

# ========================================
#  T R O U B L E S H O O T I N G
# ========================================
k get pods <pod_name> -o yaml
k describe pods <resource_name>
k logs <pod_name> -c <container_name>
k exec -it <pod_name> -- bash

# Inside the pod
apt install curl
curl localhost


# ========================================
#  R E S O U R C E S
# ========================================
minikube addons enable metrics-server
k top node
k top pod


# ----------
# General
# ----------
aws configure


# ----------
# EC2
# ----------
# Create a new policy for the IAM user, and declare the following
{
  "Version": "2012-10-17",
  "Statement": [
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
    --security-group-ids sg-078bc097372cbfde5 \
    --block-device-mappings '[{"DeviceName":"/dev/sda1","Ebs":{"VolumeSize":20,"VolumeType":"gp2"}}]' \
    --tag-specifications 'ResourceType=instance,Tags=[{Key=vocabulary,Value=compute}]' \
    --iam-instance-profile Name=vocabulary_read_on_bucket \
    --user-data file://bin/user_data.sh

aws ec2 describe-instances \
    --instance-ids i-073d70bd09e32768a \
    --query "Reservations[0].Instances[0].State.Name"

aws ec2 describe-security-groups \
    --group-ids sg-078bc097372cbfde5

# Create an elastic IP
# Create Internet Gateway
# Associate the elastic IP to the instance
# Check the route table, and manually confirm the internet gateway
# Check the Access Control List

# Actions -> Monitor and troubleshoot -> Get system log
# Why does an elastic IP address need an internet gateway, and a standard IP address does not?
# How can I know if my instance is on a private or public network?

# Use '-' in the IP address, not '.'
ssh -i conf/voc_ssh_key_1.pem ubuntu@ec2-13-38-246-147.eu-west-3.compute.amazonaws.com


# Download frfom s3
aws s3 cp s3://vocabulary-benito/vocabulary /home/ubuntu/vocabulary --recursive


# ----------
# S3
# ----------
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

