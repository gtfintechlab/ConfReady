#!/bin/bash

# Remove the existing conda environment if it exists
if conda env list | grep -q "confready_env"; then
  conda env remove -n confready_env
fi

# Create conda environment if it doesn't exist
if ! conda env list | grep "confready_env"; then
  conda env create -f environment.yml
fi

# Initialize conda (necessary for non-interactive shells)
source $(conda info --base)/etc/profile.d/conda.sh

# Activate the environment
conda activate confready_env

# Install npm dependencies
npm install --prefix ./confready

# Check if .env file already exists, if not, create it
if [ ! -f server/.env ]; then
  cat <<EOL > server/.env
TOGETHERAI_API_KEY=your_together_ai_key_here
OPENAI_API_KEY=your_openai_key_here
EOL
else
  echo ".env file already exists in server subfolder, skipping creation."
fi