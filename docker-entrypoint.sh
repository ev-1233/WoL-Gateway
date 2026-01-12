#!/bin/bash
set -e

CONFIG_FILE="/app/WOL_Brige.config"

# Check if configuration file exists
if [ ! -f "$CONFIG_FILE" ]; then
    echo "======================================"
    echo "   First Time Setup"
    echo "======================================"
    echo ""
    echo "No configuration found. Running setup..."
    echo ""
    
    # Run setup script interactively
    python3 /app/setup_wol.py
    
    echo ""
    echo "Setup complete! Starting WOL Gateway..."
    echo ""
fi

# Start the application
exec python3 -u /app/wol_gatway.py
