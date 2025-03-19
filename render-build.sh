#!/bin/bash
echo "Removing old dependencies..."
rm -rf /opt/render/project/.venv  # Remove virtual environment

echo "Reinstalling dependencies..."
pip install --no-cache-dir --force-reinstall -r requirements.txt

echo "Ensuring correct PyJWT version..."
pip uninstall -y PyJWT
pip install --no-cache-dir PyJWT==2.6.0
