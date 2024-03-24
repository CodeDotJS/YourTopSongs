#!/bin/bash

echo "Installing packages..."

pip install -q -r requirements.txt

echo "Clearing data..."

if [ ! -d "data" ]; then
    mkdir data
else
    rm -rf data/*
fi

echo "Started scraping..."

python scraper/wrapped.py

echo "Running server..."

python main.py
