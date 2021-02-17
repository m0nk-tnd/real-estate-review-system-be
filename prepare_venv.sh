#!/bin/bash

venv_dir=venv
venv_installed=false

if [[ ! -d "$venv_dir" ]]
then
  echo "Create virtual environment..."
  if ! command -v virtualenv "$venv_dir" &> /dev/null
  then
    echo "Install virtualenv before running this script!"
  else
    virtualenv "$venv_dir"
    venv_installed=true
  fi
fi

if [ "$venv_installed" = true ]
then
  source venv/bin/activate
  if [[ -f "requirements.txt" ]]
  then
    echo "Install dependencies from requirements.txt..."
    pip install -r requirements.txt
  fi
fi
