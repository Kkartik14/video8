#!/bin/bash

# Cleanup script for video8 project

echo "Cleaning up redundant and unnecessary files..."

# Remove duplicate Python files from root directory
echo "Removing redundant Python files..."
rm -f main.py groq_handler.py llm_handler.py scene_generator.py

# Remove __pycache__ directories
echo "Removing Python cache files..."
find . -name "__pycache__" -type d -exec rm -rf {} +

# Clear media directory (test files)
echo "Clearing media directory..."
rm -rf media

# Clean up generated output files (optional - comment out if you want to keep)
echo "Cleaning up generated output files..."
rm -rf outputs/videos/*
rm -rf outputs/texts/*
rm -rf outputs/Tex/*
rm -rf outputs/scripts/*
# Keep the directories but remove contents
mkdir -p outputs/videos outputs/texts outputs/Tex outputs/scripts

echo "Cleanup complete!" 