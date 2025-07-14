#!/bin/bash
# Omniscient AI Pipeline Installer

echo "🔧 Setting up Omniscient AI Pipeline..."

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Upgrade pip and install required libraries
pip install --upgrade pip
pip install transformers langchain accelerate

echo "✅ Installation complete. To run:"
echo "source venv/bin/activate && python main.py"
