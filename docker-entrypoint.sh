#!/bin/bash
set -e

CONFIG_FILE="/app/WOL_Brige.config"
ADMIN_CONFIG_FILE="/app/admin_config.json"

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

# Create default admin config if it doesn't exist
if [ ! -f "$ADMIN_CONFIG_FILE" ]; then
    echo '{"admin_enabled": false, "admin_username": "admin", "admin_password_hash": "", "2fa_enabled": false, "2fa_secret": ""}' > "$ADMIN_CONFIG_FILE"
fi

# Start the application
exec python3 -u /app/wol_gatway.py
