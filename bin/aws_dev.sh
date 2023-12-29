
# ========================================
#  G E N E R A L
# ========================================
aws configure


# ========================================
#  D A T A   &   S O U R C E   C O D E
# ========================================
aws s3 sync \
    /home/benoit/Documents/vocabulary \
    s3://vocabulary-benito/vocabulary \
    --exclude ".pytest_cache/*" \
    --exclude ".vscode/*" \
    --exclude "__pycache__/*" \
    --exclude ".git/*" \
    --exclude "bin/*" \
    --exclude "common/*" \
    --exclude "conf/*" \
    --exclude "data/__pycache__/*" \
    --exclude "divers/*" \
    --exclude "doc/*" \
    --exclude "env/*" \
    --exclude "htmlcov/*" \
    --exclude "logs/*" \
    --exclude "mgmt/*" \
    --exclude "scripts/*" \
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
    --delete


aws s3 sync \
    s3://vocabulary-benito/vocabulary \
    /home/ubuntu/vocabulary \
    --exclude "env/*" \
    --delete \
    --debug

aws s3 cp \
    /home/benoit/Documents/vocabulary/src/web_app.py \
    s3://vocabulary-benito/vocabulary/src/web_app.py

aws s3 cp \
    s3://vocabulary-benito/vocabulary/src/web_app.py \
    /home/ubuntu/vocabulary/src/web_app.py

# Depuis Fedora à l'EC2
scp -r -i \
    conf/voc_ssh_key_1.pem \
    /home/benoit/Documents/vocabulary/src/ \
    ubuntu@ec2-51-44-1-83.eu-west-3.compute.amazonaws.com:/home/ubuntu/vocabulary/



# =======================
#  C O N N E C T
# =======================
# Use '-' in the IP address, not '.'
ssh -i  \
    conf/voc_ssh_key_1.pem \
    ubuntu@ec2-51-44-1-83.eu-west-3.compute.amazonaws.com



# =======================
#  P Y T H O N
# =======================
export PYTHONPATH=/home/ubuntu/vocabulary/src:$PYTHONPATH
cd vocabulary
python3 -m venv env
source env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt



# =======================
#  R U N
# =======================
cd ~/vocabulary
uvicorn src.web_app:app --reload --port 8080 --host 0.0.0.0



# ==============================================
#  T R O U B L E S H O O T I N G
# ==============================================
pkill uvicorn
