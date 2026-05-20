#!/bin/bash

# Set expiry date and time (YYYY-MM-DD HH:MM)
EXPIRY="2026-05-22 18:00"

NOW=$(date +"%Y-%m-%d %H:%M")

if [[ "$NOW" > "$EXPIRY" ]]; then
    echo "========================================"
    echo " Trial period has expired."
    echo " Expired on: $EXPIRY"
    echo " Please contact support to continue."
    echo "========================================"
    exit 1
fi

echo "Trial valid until: $EXPIRY"
python3 -m streamlit run app_tally.py
