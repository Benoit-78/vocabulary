#!/bin/bash

# --------------------------------------------------------------------------------
#  /!\  I M P O R T A N T  /!\
# A shell script created on Windows may not work properly on Linux.
# Here are the commands to make it work on Linux:
# sudo apt-get install dos2unix
# dos2unix -b pip.sh
# If dos2unix cannot be installed, then create an empty shell file in Linux,
# then copy-paste the content of the Windows file in the Linux file.
# --------------------------------------------------------------------------------

# Check script argument
if [ $# -eq 0 ]; then
    echo "# ERROR: No environment name provided. Usage: $0 <environment_name>"
    exit 1
fi

# Deactivating current environment
echo "# INFO: Deactivating current environment..."
source deactivate
echo "# --------------------------------------------------------------------------------"

# Upgrading pip
echo "# INFO: Upgrading pip..."
python3 -m pip install --upgrade pip
echo "# --------------------------------------------------------------------------------"

# Installing virtualenv
echo "# INFO: Installing virtualenv..."
python3 -m pip install virtualenv
echo "# --------------------------------------------------------------------------------"

# Creating the virtual environment
echo "# INFO: Creating the virtual environment..."
python3 -m venv ${1}
echo "# --------------------------------------------------------------------------------"

# Activating the virtual environment
echo "# INFO: Activating the virtual environment..."
source ${1}/bin/activate
echo "# --------------------------------------------------------------------------------"

# Upgrading pip
echo "# INFO: Upgrading pip..."
python3 -m pip install --upgrade pip
echo "# --------------------------------------------------------------------------------"

# Installing libraries
echo "# INFO: Installing libraries..."

# API
pip install fastapi==0.103.0
echo "# -------------------------"
pip install fastapi-sessions==0.3.2
echo "# -------------------------"
pip install "python-jose[cryptography]"  # for JWT
echo "# -------------------------"
pip install "passlib[bcrypt]" ##################
echo "# -------------------------"
pip install python-multipart==0.0.9
echo "# -------------------------"
pip install anyio==3.7.1
echo "# -------------------------"
pip install h11==0.14.0
echo "# -------------------------"
pip install idna==3.4
echo "# -------------------------"
pip install Jinja2==3.1.2
echo "# -------------------------"
pip install lazy-object-proxy==1.9.0
echo "# -------------------------"
pip install MarkupSafe==2.1.3
echo "# -------------------------"
pip install sniffio==1.3.0
echo "# -------------------------"
pip install starlette==0.27.0
echo "# -------------------------"
pip install urllib3==1.26.16
echo "# -------------------------"
pip install uvicorn==0.23.2
echo "# -------------------------"
pip install itsdangerous==2.1.2
echo "# -------------------------"

# Visualization
pip install plotly==5.18.0
echo "# -------------------------"

# Cloud (better not to fix the version)
pip install awscli
echo "# -------------------------"
pip install botocore
echo "# -------------------------"
pip install s3transfer
echo "# -------------------------"

# Database
#   pip install mysql==0.0.3  #############
pip install mysql-connector-python==8.1.0
echo "# -------------------------"
pip install mysqlclient>=2.0.1,<2.2.0
echo "# -------------------------"
pip install PyMySQL==1.1.0
echo "# -------------------------"
pip install SQLAlchemy==2.0.20
echo "# -------------------------"
pip install redis==5.0.3
echo "# -------------------------"

# Data processing
pip install numpy==1.25.0
echo "# -------------------------"
pip install pandas==2.0.2
echo "# -------------------------"
pip install python-dateutil==2.8.2
echo "# -------------------------"
pip install pytz==2023.3
echo "# -------------------------"
pip install tzdata==2023.3
echo "# -------------------------"

# Python
pip install pydantic==2.3.0
echo "# -------------------------"
pip install pydantic_core==2.6.3
echo "# -------------------------"
pip install python-dotenv==1.0.1
echo "# -------------------------"

# Continuous integration
pip install isort==5.12.0
echo "# -------------------------"
pip install ruff==0.3.0
echo "# -------------------------"
pip install pytest==7.4.3
echo "# -------------------------"
pip install coverage==7.4.3
echo "# -------------------------"


# Logs
pip install loguru==0.7.2
echo "# -------------------------"

# Development Tools
pip install altgraph==0.17.3
echo "# -------------------------"
pip install annotated-types==0.5.0
echo "# -------------------------"
pip install astroid==3.1.0
echo "# -------------------------"
pip install asttokens==2.4.0
echo "# -------------------------"
pip install click==8.1.7
echo "# -------------------------"
pip install executing==1.2.0
echo "# -------------------------"
pip install mccabe==0.7.0
echo "# -------------------------"
pip install pefile==2023.2.7
echo "# -------------------------"
pip install platformdirs==3.8.0
echo "# -------------------------"
pip install wrapt==1.15.0
echo "# -------------------------"
pip install colorama==0.4.4
echo "# -------------------------"
pip install Pygments==2.16.1
echo "# -------------------------"
pip install tk==0.1.0
echo "# -------------------------"
pip install typing_extensions==4.7.1
echo "# -------------------------"

# Serialization / Configuration
pip install PyYAML==6.0.1
echo "# -------------------------"
pip install protobuf==4.21.12
echo "# -------------------------"
pip install tomlkit==0.11.8
echo "# -------------------------"

# Documentation
pip install docutils==0.16
echo "# -------------------------"

# Concurrency
pip install greenlet==2.0.2
echo "# -------------------------"
pip install dill==0.3.6
echo "# -------------------------"

# JSONPath Expression
pip install jmespath==1.0.1
echo "# -------------------------"

# Cryptography
pip install rsa==4.7.2
echo "# -------------------------"

# Compatibility
pip install pywin32-ctypes==0.2.1
echo "# -------------------------"
pip install six==1.16.0
echo "# -------------------------"
pip install win32-setctime==1.1.0

echo "# --------------------------------------------------------------------------------"

# Extract the logs and identify the "uninstalled"

# Provisioning the environment to Jupyter notebooks
# echo "# INFO: Provisioning the environment to jupyter notebooks"
# python -m ipykernel install --user --name ${1} --display-name ${1}
# echo "# --------------------------------------------------------------------------------"

# Ending message
bash ${1}/bin/activate
echo "# INFO: Pip environment ${1} ready!"

# End of life
# echo "# INFO: Removing the virtual environment..."
# deactivate
# rm -r ~/work/${1}
# echo "# INFO: Removing the jupyter kernel..."
# jupyter kernelspec remove ${1}
# echo "# INFO: Virtual environment completetly removed (snif snif...)"



# ======================
#  U T I L I T I E S
# ======================
#pip list

#pip freeze > requirement.txt

#pip show numpy

#pip check

#pip uninstall <package>