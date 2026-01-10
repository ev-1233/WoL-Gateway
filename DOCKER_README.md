# WOL Gateway - Docker Setup

## Quick Start

### 1. Build and Run with Docker Compose (Recommended)
```bash
# Build and start the container
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the container
docker-compose down
```

### 2. Build and Run with Docker directly
```bash
# Build the image
docker build -t wol-gateway .

# Run the container
docker run -d --name wol-gateway --network host wol-gateway

# View logs
docker logs -f wol-gateway

# Stop and remove
docker stop wol-gateway && docker rm wol-gateway
```

## Updating Configuration

After changing `WOL_Brige.config`:
```bash
# With docker-compose
docker-compose restart

# With docker
docker restart wol-gateway
```

## Benefits of Docker Setup

✅ **No dependency issues** - Everything is bundled in the container  
✅ **No sudo needed** - Docker handles port binding  
✅ **Works on all Linux distros** - Same container everywhere  
✅ **Easy updates** - Just rebuild and restart  
✅ **Automatic restart** - Container restarts if it crashes  
✅ **Clean uninstall** - Remove container, no leftover files

## Accessing the Gateway

Once running, access:
- Local: http://localhost:500/wake
- Network: http://YOUR_IP:500/wake

## Troubleshooting

### Check if Docker is running:
```bash
docker ps
```

### View container logs:
```bash
docker-compose logs -f
```

### Rebuild after code changes:
```bash
docker-compose up -d --build
```
