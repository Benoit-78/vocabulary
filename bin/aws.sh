
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

grep "GroupId"

aws ec2 authorize-security-group-ingress --group-id sg-08ebad99d1b1b98b6 --protocol tcp --port 22 --cidr 88.161.167.12/32
aws ec2 authorize-security-group-ingress --group-id sg-08ebad99d1b1b98b6 --protocol tcp --port 8080 --cidr 0.0.0.0/0
aws ec2 authorize-security-group-ingress --group-id sg-08ebad99d1b1b98b6 --protocol tcp --port 80 --cidr 0.0.0.0/0
# aws ec2 authorize-security-group-ingress --group-id sg-08ebad99d1b1b98b6 --protocol tcp --port 3306 --cidr 0.0.0.0/0
aws ec2 authorize-security-group-egress --group-id sg-08ebad99d1b1b98b6 --protocol tcp --port 3306 --cidr 0.0.0.0/0


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

aws s3 sync \
    /home/benoit/Documents/vocabulary \
    s3://vocabulary-benito/vocabulary \
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
    --exclude "*.pdf" \
    --exclude "*.png" \
    --exclude "*.pyc" \
    --exclude "*.txt"



aws ec2 run-instances \
    --image-id ami-00983e8a26e4c9bd9 \
    --instance-type t2.medium \
    --key-name voc_ssh_key_1 \
    --security-group-ids sg-08ebad99d1b1b98b6 \
    --block-device-mappings '[{"DeviceName":"/dev/sda1","Ebs":{"VolumeSize":20,"VolumeType":"gp2"}}]' \
    --tag-specifications 'ResourceType=instance,Tags=[{Key=vocabulary,Value=compute}]' \
    --iam-instance-profile Name=vocabulary_read_on_bucket \
    --user-data file://bin/user_data.sh

grep InstanceId

aws ec2 describe-instances \
    --instance-ids i-0d346ee03d9c2524e \
    --query "Reservations[0].Instances[0].State.Name"

# Create Internet Gateway
aws ec2 create-internet-gateway

grep InternetGatewayId

aws ec2 attach-internet-gateway --internet-gateway-id igw-067bdaf3b90f544d8 --vpc-id vpc-0011e2cd73034beb9

# Create an elastic IP
aws ec2 allocate-address \
    --domain vpc

grep PublicIp
grep AllocationId

aws ec2 associate-address \
    --allocation-id eipalloc-0188ef3e338bdd852 \
    --instance-id i-0d346ee03d9c2524e
# Check the route table, and manually confirm the internet gateway
# Check the Access Control List
# Actions -> Monitor and troubleshoot -> Get system log
# Why does an elastic IP address need an internet gateway, and a standard IP address does not?
# How can I know if my instance is on a private or public network?

# Use '-' in the IP address, not '.'
ssh -i conf/voc_ssh_key_1.pem ubuntu@ec2-15-236-44-153.eu-west-3.compute.amazonaws.com



# =======================
# User data
# =======================
sudo apt-get update
sudo apt-get install -y awscli
sudo apt-get install -y default-libmysqlclient-dev
sudo apt-get install -y python3
sudo apt-get install -y python3-pip
sudo apt-get install -y python3-venv
sudo apt-get install -y mariadb-client
sudo apt-get install -y uvicorn
# sudo apt-get install -y pkg-config
# sudo apt-get install -y libssl-dev
# sudo apt-get install -y build-essential



# =======================
# Environment
# =======================
# Packages
sudo apt-get update -y
sudo apt-get install -y awscli
sudo apt-get install -y default-libmysqlclient-dev
# On Red Hat-based systems
# sudo dnf install mysql-devel
sudo apt-get install -y python3-pip
sudo apt-get install -y python3-venv
sudo apt-get install -y uvicorn
sudo apt-get install -y nginx

# Data
aws s3 sync \
    s3://vocabulary-benito/vocabulary \
    /home/ubuntu/vocabulary

# Python
export PYTHONPATH=/home/ubuntu/vocabulary/src:$PYTHONPATH
cd vocabulary
python3 -m venv env
source env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt



# =======================
# Nginx
# =======================
sudo nano /etc/nginx/sites-available/vocabulary_app.com
# Copy this
server {
    listen 443;
    server_name vocabulary-app.com www.vocabulary-app.com;

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
sudo ln -s /etc/nginx/sites-available/vocabulary_app.com /etc/nginx/sites-enabled/
sudo service nginx restart



# =======================
# MariaDB
# =======================
sudo apt-get install -y mariadb-client
sudo apt-get install -y mariadb-server
cd ~/vocabulary/data
sudo mariadb
SOURCE english.sql;
SOURCE zhongwen.sql;
SELECT user, host FROM mysql.user;
SHOW GRANTS FOR 'benito'@'localhost';
ALTER USER 'benito'@'localhost' IDENTIFIED BY '<database_password>';

uvicorn src.web_app:app --reload --port 8080 --host 0.0.0.0



# =======================
# Troubleshooting
# =======================
# S3
aws s3 rm s3://vocabulary-benito/vocabulary/logs \
    --recursive
aws s3 rm s3://vocabulary-benito/vocabulary/bin/aws_commands.sh
# Nginx
sudo service nginx status
sudo tail -f /var/log/nginx/error.log



# =======================
#  E C R
# =======================
aws ecr get-login-password --region eu-west-3 | docker login --username AWS --password-stdin 098964451146.dkr.ecr.eu-west-3.amazonaws.com
# docker build -t vocabulary .
docker-compose build
docker tag vocabulary_web:latest public.ecr.aws/e8w4p1y9/vocabulary_compose:latest
#docker tag vocabulary_web:latest 098964451146.dkr.ecr.eu-west-3.amazonaws.com/vocabulary_web:latest
#docker push 098964451146.dkr.ecr.eu-west-3.amazonaws.com/vocabulary_compose:latest
docker push public.ecr.aws/e8w4p1y9/vocabulary_compose:latest



# =======================
# End of life
# =======================
aws ec2 terminate-instances \
    --instance-ids <instance-id>

aws ec2 release-address \
    --allocation-id <alloc-id>


