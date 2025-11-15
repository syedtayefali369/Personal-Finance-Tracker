#!/bin/bash

echo "Setting up Personal Finance Tracker..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3.8 or higher from https://python.org"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
REQUIRED_VERSION="3.8"

if [ $(echo "$PYTHON_VERSION >= $REQUIRED_VERSION" | bc -l) -eq 1 ]; then
    echo "Python $PYTHON_VERSION detected - compatible"
else
    echo "Python $PYTHON_VERSION detected - requires $REQUIRED_VERSION or higher"
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Setup completed successfully!"
echo ""
echo "To run the application:"
echo "  source venv/bin/activate"
echo "  python main.py"
echo ""
echo "Or use the run script: ./run.sh"