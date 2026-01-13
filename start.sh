#!/bin/bash
# WOL Gateway Startup Script
# This script handles all the complexity of starting the gateway

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "========================================="
echo "    WOL Gateway Startup Script"
echo "========================================="

# Check if running as root (for low ports)
if [ "$EUID" -ne 0 ]; then
    echo -e "${YELLOW}Note: Not running as root. Will use sudo for privileged ports.${NC}"
    SUDO="sudo"
else
    SUDO=""
fi

# Install Python wakeonlan if not present
if ! $SUDO python3 -c "import wakeonlan" 2>/dev/null; then
    echo -e "${YELLOW}Installing wakeonlan Python package...${NC}"
    $SUDO pip3 install wakeonlan
fi

# Check if config exists
if [ ! -f "WOL_Brige.config" ]; then
    echo -e "${RED}Error: WOL_Brige.config not found!${NC}"
    echo "Please run setup_wol.py first."
    exit 1
fi

# Kill any existing instances
echo "Checking for existing instances..."
$SUDO pkill -f "python.*wol_gatway.py" 2>/dev/null
sleep 1

# Start the gateway
echo -e "${GREEN}Starting WOL Gateway...${NC}"
$SUDO python3 wol_gatway.py

