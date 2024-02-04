
# ===========================================
#  G E N E R A L
# ===========================================
aws configure



# ===========================================
#  I A M
# ===========================================
# Users
aws iam update-user \
    --user-name vocabulary_test \
    --new-user-name voc_tester

# Roles
aws iam attach-role-policy \
    --role-name vocabulary_read_on_bucket \
    --policy-arn arn:aws:iam::aws:policy/AmazonEC2FullAccess

aws iam list-attached-role-policies \
    --role-name vocabulary_read_on_bucket

aws iam attach-role-policy \
    --role-name logger \
    --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess

# Set the IAM role for the ALB
aws elbv2 set-load-balancer-attributes \
    --load-balancer-arn your-alb-arn \
    --attributes Key=access_logs.s3.enabled,Value=true Key=access_logs.s3.bucket,Value=vocabulary-benito Key=access_logs.s3.prefix,Value=alb-logs/

# ==============================================
#  S 3
# ==============================================
aws s3 rm s3://vocabulary-benito/vocabulary/logs \
    --recursive
aws s3 rm s3://vocabulary-benito/vocabulary/bin/aws_commands.sh

echo '{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "elasticloadbalancing.amazonaws.com"
      },
      "Action": "s3:PutObject",
      "Resource": "arn:aws:s3:::vocabulary-benito/logs*"
    }
  ]
}' > conf/s3/bucket-policy.json

aws s3api put-bucket-policy \
    --bucket vocabulary-benito \
    --policy file://conf/s3/bucket-policy.json

# ===========================================
#  E C 2
# ===========================================

# ----- Security groups -----
# ALB
aws ec2 create-security-group \
    --group-name YourALBSecurityGroup \
    --description "ALB Security Group" \
    --vpc-id YourVpcId

grep GroupId

aws ec2 describe-security-groups --group-ids <alb-sg-id>

aws ec2 authorize-security-group-ingress \
    --group-id <alb-sg-id> \
    --protocol tcp \
    --port 80 \
    --cidr 0.0.0.0/0

aws ec2 authorize-security-group-ingress \
    --group-id <alb-sg-id> \
    --protocol tcp \
    --port 443 \
    --cidr 0.0.0.0/0

# Instances
aws ec2 create-security-group \
    --group-name vocabulary-sg \
    --description "Allows users to access the application" \
    --vpc-id vpc-0011e2cd73034beb9

aws ec2 authorize-security-group-ingress \
    --group-id <inst-sg-id> \
    --protocol tcp \
    --port 22 \
    --cidr <IP-address>/32

aws ec2 authorize-security-group-ingress \
    --group-id <inst-sg-id> \
    --protocol tcp \
    --port 80 \
    --source-security-group <alb-sg-id>

aws ec2 authorize-security-group-ingress \
    --group-id <inst-sg-id> \
    --protocol tcp \
    --port 443 \
    --source-security-group <alb-sg-id>



# ----- Key pair -----
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

grep InstanceId

aws ec2 describe-instances \
    --instance-ids i-0d346ee03d9c2524e \
    --query "Reservations[0].Instances[0].State.Name"

# ----- Internet Gateway -----
aws ec2 create-internet-gateway

grep InternetGatewayId

aws ec2 attach-internet-gateway \
    --internet-gateway-id igw-067bdaf3b90f544d8 \
    --vpc-id vpc-0011e2cd73034beb9

# ----- Elastic IP -----
aws ec2 allocate-address \
    --domain vpc

grep PublicIp
grep AllocationId

aws ec2 associate-address \
    --allocation-id eipalloc-0e1af7a0b11f39ef7 \
    --instance-id i-000d897a34bbabc2b
# Check the route table, and manually confirm the internet gateway
# Check the Access Control List
# Actions -> Monitor and troubleshoot -> Get system log
# Why does an elastic IP address need an internet gateway, and a standard IP address does not?
# IP like 10.*.*.* : private
# IP like 172.*.*.* : public

aws ec2 terminate-instances \
    --instance-ids <instance-id>

aws ec2 release-address \
    --allocation-id <alloc-id>



# ==============================================
#  E C R
# ==============================================
aws ecr get-login-password --region eu-west-3 | docker login --username AWS --password-stdin 098964451146.dkr.ecr.eu-west-3.amazonaws.com
# docker build -t vocabulary .
docker-compose build
docker tag vocabulary_web:latest public.ecr.aws/e8w4p1y9/vocabulary_compose:latest
#docker tag vocabulary_web:latest 098964451146.dkr.ecr.eu-west-3.amazonaws.com/vocabulary_web:latest
#docker push 098964451146.dkr.ecr.eu-west-3.amazonaws.com/vocabulary_compose:latest
docker push public.ecr.aws/e8w4p1y9/vocabulary_compose:latest



# ==============================================
#  S Y S T E M   P A C K A G E S
# ==============================================
sudo apt-get update -y
sudo apt-get install -y awscli
sudo apt-get install -y default-libmysqlclient-dev
sudo apt-get install -y mariadb-client
sudo apt-get install -y mariadb-server
sudo apt-get install -y python3
sudo apt-get install -y python3-pip
sudo apt-get install -y python3-venv
sudo apt-get install -y uvicorn
sudo apt-get install -y nginx



# ==============================================
#  MAKE THE APP AVAILABLE
# ==============================================
# Create a hosted zone
aws route53 create-hosted-zone \
    --name vocabulary-app.com \
    --caller-reference $(date +%s) \
    --query 'HostedZone.{Id:Id}' \
    --output text

# Create an Application Load Balancer
aws elbv2 create-load-balancer \
    --name vocabulary-lb \
    --subnets subnet-0e199c3602e3ff025 subnet-057a87ac7a13cf0fe \
    --security-groups sg-0ee3fc8193e601c90 \
    --scheme internet-facing \
    --output json

aws elbv2 modify-load-balancer-attributes \
    --load-balancer-arn arn:aws:elasticloadbalancing:eu-west-3:098964451146:loadbalancer/app/vocabulary-lb/5f3a61e3ac69c794 \
    --attributes Key=access_logs.s3.enabled,Value=true Key=access_logs.s3.bucket,Value=bucket-name Key=access_logs.s3.prefix,Value=prefix Key=deletion_protection.enabled,Value=true

# Access Load Balancer logs
aws elbv2 describe-load-balancers \
    --names vocabulary-lb

# Create a target group
aws elbv2 create-target-group \
    --name vocabulary-tg \
    --protocol HTTP \
    --port 80 \
    --vpc-id vpc-0a7070d446d46681b \
    --output json

# Register Targets (Instances) with the Target Group:
aws elbv2 register-targets \
    --target-group-arn YourTargetGroupArn \
    --targets Id=i-xxxxxxxx Id=i-yyyyyyyy

# Create an HTTP listener
aws elbv2 create-listener \
    --load-balancer-arn arn:aws:elasticloadbalancing:eu-west-3:098964451146:loadbalancer/app/vocabulary-lb/5f3a61e3ac69c794 \
    --protocol HTTP \
    --port 80 \
    --default-actions Type=forward,TargetGroupArn=arn:aws:elasticloadbalancing:eu-west-3:098964451146:targetgroup/vocabulary-tg/0575f75560cffcc6 \
    --output json

# Create an HTTPS listener
aws elbv2 create-listener \
    --load-balancer-arn arn:aws:elasticloadbalancing:eu-west-3:098964451146:loadbalancer/app/vocabulary-lb/5f3a61e3ac69c794 \
    --protocol HTTPS \
    --port 443 \
    --certificates CertificateArn=arn:aws:acm:eu-west-3:098964451146:certificate/debcc9b7-3bb5-4c87-b319-fcdd9123536d \
    --default-actions Type=forward,TargetGroupArn=arn:aws:elasticloadbalancing:eu-west-3:098964451146:targetgroup/vocabulary-tg/0575f75560cffcc6 \
    --output json

# Create a Route53 record pointing to the ALB
aws route53 change-resource-record-sets \
    --hosted-zone-id Z07747923RSGBESFDLWVX \
    --change-batch '{
        "Changes": [
            {
                "Action": "CREATE",
                "ResourceRecordSet": {
                    "Name": "www.vocabulary-app.com",
                    "Type": "CNAME",
                    "TTL": 300,
                    "ResourceRecords": [
                        {
                            "Value": "vocabulary-lb-1646646983.eu-west-3.elb.amazonaws.com"
                        }
                    ]
                }
            }
        ]
    }'



# ==============================================
#  N G I N X
# ==============================================
sudo nano /etc/nginx/sites-available/vocabulary_app.com

server {
    listen 80;
    server_name vocabulary-app.com www.vocabulary-app.com;

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

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

sudo service nginx status
sudo tail -f /var/log/nginx/error.log
