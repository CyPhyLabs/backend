#!/bin/bash

# Function to handle errors
handle_error() {
    echo "Error on line $1"
    exit 1
}

# Trap errors and call handle_error
trap 'handle_error $LINENO' ERR

# Load environment variables from .setup.env file
if [ ! -f .setup.env ]; then
    echo ".setup.env file not found!"
    exit 1
fi
source .setup.env

# Install PostgreSQL
if ! command -v brew &> /dev/null; then
    echo "Homebrew not found, please install it first."
    exit 1
fi
brew install postgresql

# Start PostgreSQL service
brew services start postgresql

# Wait for PostgreSQL to start
sleep 5

# Check if PostgreSQL role exists
ROLE_EXISTS=$(psql postgres -tAc "SELECT 1 FROM pg_roles WHERE rolname='$POSTGRES_USER'")
if [ "$ROLE_EXISTS" != "1" ]; then
    echo "Creating PostgreSQL role: $POSTGRES_USER"
    psql postgres -c "CREATE ROLE $POSTGRES_USER WITH LOGIN PASSWORD '$POSTGRES_PASSWORD';"
    psql postgres -c "ALTER ROLE $POSTGRES_USER CREATEDB;"
else
    echo "PostgreSQL role already exists"
fi

# Check if the conda environment exists
ENV_NAME=$(grep name environment.yml | cut -d ' ' -f 2)
if conda env list | grep -q $ENV_NAME; then
    echo "Updating existing conda environment: $ENV_NAME"
    conda env update -f environment.yml
else
    echo "Creating new conda environment: $ENV_NAME"
    conda env create -f environment.yml
fi

# Make the script executable
chmod +x setup.sh

# Activate the conda environment
echo "Activating conda environment: $ENV_NAME"
source $(conda info --base)/etc/profile.d/conda.sh
conda activate $ENV_NAME

# Make migrations
python t2t_api/manage.py makemigrations
python t2t_api/manage.py migrate 

echo "Setup complete."