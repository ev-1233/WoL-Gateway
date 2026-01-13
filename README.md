# WOL Gateway

Wake-on-LAN gateway service that provides a simple web interface to wake up your servers remotely form anywhere without a vpn.

## Features



## Installation

### Option 1: Docker Hub (Strongly Recommended)

**Prerequisites:** Docker installed and running

```bash
docker run -it --name wol-gateway \ --cap-add NET_ADMIN --cap-add NET_RAW \ --network host  \ --restart unless-stopped \ ev1233/wol-gateway:latest
```

The setup script will:
- Help you configure your servers (MAC addresses, URLs, etc.)
- Build and start the Docker container automatically
- Set up auto-restart on failure

### Option 2: Standalone Executable (No Installation Required)


1. Download the latest executable for your system:
   - [Linux](https://github.com/ev1233/wol-gateway/releases/latest/download/wol-gateway-linux)
   - [Windows](https://github.com/ev1233/wol-gateway/releases/latest/download/wol-gateway-windows.exe)
   - [macOS](https://github.com/ev1233/wol-gateway/releases/latest/download/wol-gateway-macos)

2. Run the executable:
   ```bash
   # Linux/macOS
   chmod +x wol-gateway-linux
   ./wol-gateway-linux
   
   # Windows
   wol-gateway-windows.exe
   ```

3. Follow the on-screen prompts to configure your servers

## Install with git
If you just love git that much:

**python3 must be installed and we highly recomend you install docker(technically optional)**

```bash
# Pull the latest release
LATEST_VERSION=$(curl -s https://api.github.com/repos/ev1233/WoL-Gateway/releases/latest | grep "tag_name" | cut -d '"' -f 4)
wget https://github.com/ev1233/WoL-Gateway/archive/refs/tags/$LATEST_VERSION.tar.gz -O wol-gateway-latest.tar.gz

# Decompress the file
tar --transform='s/^WoL-Gateway-.*/WoL-Gateway/' -xzf wol-gateway-latest.tar.gz

# Navigate to the folder
cd WoL-Gateway

python3 setup_wol.py

# Decompress the file
tar --transform='s/^WoL-Gateway-0.6.1/WoL-Gateway/' -xzf wol-gateway-latest.tar.gz

# Navigate to the folder
cd WoL-Gateway

python3 setup_wol.py
```

## Updating

### Docker
```bash
docker pull ev1233/wol-gateway:latest
docker compose down && docker compose up -d
```

### Standalone Executable
Download the latest version from [Releases](https://github.com/ev1233/wol-gateway/releases/latest)

### Github install
```bash
git pull
python3 setup_wol.py
```

## Troubleshooting

### Wake-on-LAN not working?

1. Enable WOL in your server's BIOS/UEFI
2. Enable WOL in your network card settings
3. Ensure both devices are on the same network/subnet
4. Check firewall rules allow UDP port 9 (WOL magic packet)

### Docker container won't start?

```bash
# Check logs
docker logs wol-gateway

# Verify Docker has network capabilities
docker inspect wol-gateway | grep CapAdd
```

## Development

```bash
# Clone repository
git clone https://github.com/ev1233/wol-gateway.git
cd wol-gateway

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install flask wakeonlan

# Run directly
python3 wol_gatway.py
```

