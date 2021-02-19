#!/bin/bash

venv_dir=venv
venv_installed=false
venv_activated=false

if [[ ! -d "$venv_dir" ]]
then
  echo "Create virtual environment..."
  if python3 -c 'import venv'
  then
    python3 -m venv "$venv_dir"
    venv_installed=true
  else
    echo "Install python3-venv before running this script!"
  fi
fi

if [ "$venv_installed" = true ]
then
  if [[ -f venv/bin/activate ]]
  then
    source venv/bin/activate
    venv_activated=true
  else
    if [[ -f venv/Scripts/activate ]]
    then
      source venv/Scripts/activate
      venv_activated=true
    else
      echo "Neither venv/bin/activate nor venv/Scripts/activate was found. Skip dependencies installation."
    fi
  fi
  if [ venv_activated = true ]
  then
    if [[ -f "requirements.txt" ]]
    then
      echo "Install dependencies from requirements.txt..."
      pip install -r requirements.txt
    fi
  fi
fi
