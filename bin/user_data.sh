apt-get update
apt-get install -y pkg-config
apt-get install -y default-libmysqlclient-dev
apt-get install -y python3-dev
apt-get install -y python3-pip
apt-get install libssl-dev
apt-get install -y build-essential
apt-get install -y mariadb-client
apt-get install awscli
snap install docker

pip install --upgrade pip
pip install --no-cache-dir -r requirements.txt
