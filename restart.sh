#!/bin/bash

# Script to cleanly restart Streamlit app after code changes

echo "🧹 Clearing Python cache..."
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null
find . -name "*.pyc" -delete 2>/dev/null

echo "✅ Cache cleared!"
echo ""
echo "🚀 Starting Streamlit..."
echo ""

streamlit run app.py
