
# ========================================
#  D A T A   &   S O U R C E   C O D E
# ========================================
# local -> S3
aws s3 cp -r \
    /home/benoit/projects/vocabulary/ \
    s3://vocabulary-benito/vocabulary/

# S3 -> EC2
aws s3 cp \
    s3://vocabulary-benito/vocabulary/src/web_app.py \
    /home/ubuntu/vocabulary/src/web_app.py



# =======================
#  C O N N E C T
# =======================
aws ec2 start-instances \
    --instance-ids i-03fae8b09bdb0587f \
    --region eu-west-3

# Use '-' in the IP address, not '.'
ssh -i  \
    conf/voc_ssh_key_1.pem \
    ubuntu@ec2-51-44-1-83.eu-west-3.compute.amazonaws.com

# local -> EC2
scp -r -i \
    conf/voc_ssh_key_1.pem \
    /home/benoit/projects/vocabulary/src/ \
    ubuntu@ec2-51-44-1-83.eu-west-3.compute.amazonaws.com:/home/ubuntu/vocabulary/

scp -r -i \
    conf/voc_ssh_key_1.pem \
    /home/benoit/projects/vocabulary/data/queries \
    ubuntu@ec2-51-44-1-83.eu-west-3.compute.amazonaws.com:/home/ubuntu/vocabulary/data/queries && cl

scp -r -i \
    conf/voc_ssh_key_1.pem \
    /home/benoit/projects/vocabulary/requirements.txt \
    ubuntu@ec2-51-44-1-83.eu-west-3.compute.amazonaws.com:/home/ubuntu/vocabulary/ && cl



# Python
# ------
export PYTHONPATH=/home/ubuntu/vocabulary/src:$PYTHONPATH
cd vocabulary
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt



# JavaScript
# ----------
npm install --save-dev jest @babel/core @babel/preset-env babel-jest
npm install --save-dev jest-environment-jsdom



# =======================
#  R U N
# =======================
# DEV
cd ~/vocabulary
sudo service redis-server stop
redis-server
uvicorn src.web_app:app \
    --port 8080 \
    --host 0.0.0.0 \
    --reload

# PROD
uvicorn src.web_app:app \
    --port 8080 \
    --host 0.0.0.0 \
    --workers 3



# ==============================================
#  T R O U B L E S H O O T I N G
# ==============================================
pkill uvicorn



# ==============================================
#  E N D   O F   L I V E
# ==============================================
aws ec2 stop-instances \
    --instance-ids i-03fae8b09bdb0587f \
    --region eu-west-3
