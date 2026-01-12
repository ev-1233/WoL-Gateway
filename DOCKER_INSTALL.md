# WOL Gateway - Quick Install (Docker)

## 🚀 One-Command Install

```bash
docker run -it --name wol-gateway \
  --cap-add NET_ADMIN --cap-add NET_RAW \
  -p 5000:5000 \
  --restart unless-stopped \
  ev1233/wol-gateway:latest
```

That's it! The setup wizard will start automatically on first run.

## What happens:

1. **First run**: Interactive setup wizard asks for:
   - Server MAC address
   - Server URL
   - Wait time
   - Port (default: 5000)

2. **Subsequent runs**: Starts immediately with saved config

## Access your gateway:

- Local: http://localhost:5000
- Network: http://YOUR_IP:5000

## Useful Commands:

```bash
# View logs
docker logs wol-gateway

# Stop
docker stop wol-gateway

# Start
docker start wol-gateway

# Restart
docker restart wol-gateway

# Remove (to reconfigure)
docker rm -f wol-gateway
# Then run the install command again
```

## Persistent Configuration

If you want to keep your config outside the container:

```bash
# Create config directory
mkdir -p ~/wol-gateway-config

# First run with volume (setup will save here)
docker run -it --name wol-gateway \
  --cap-add NET_ADMIN --cap-add NET_RAW \
  -p 5000:5000 \
  -v ~/wol-gateway-config:/app \
  --restart unless-stopped \
  ev1233/wol-gateway:latest
```

Your config is now saved in `~/wol-gateway-config/WOL_Brige.config`

## Update to Latest Version:

```bash
# Pull new version
docker pull ev1233/wol-gateway:latest

# Remove old container
docker rm -f wol-gateway

# Run with same command (config preserved if using volume)
docker run -it --name wol-gateway \
  --cap-add NET_ADMIN --cap-add NET_RAW \
  -p 5000:5000 \
  --restart unless-stopped \
  ev1233/wol-gateway:latest
```

## Docker Compose (Alternative)

Create `docker-compose.yml`:

```yaml
services:
  wol-gateway:
    image: ev1233/wol-gateway:latest
    container_name: wol-gateway
    stdin_open: true
    tty: true
    cap_add:
      - NET_ADMIN
      - NET_RAW
    ports:
      - "5000:5000"
    volumes:
      - ./config:/app
    restart: unless-stopped
```

Then:
```bash
# First run (setup)
docker compose up

# After setup, run in background
docker compose up -d
```

## Troubleshooting

**Can't access from other devices?**
```bash
sudo ufw allow 5000/tcp
```

**Want to reconfigure?**
```bash
docker rm -f wol-gateway
docker run -it --name wol-gateway ...
```

**Check if it's running:**
```bash
docker ps | grep wol-gateway
```
