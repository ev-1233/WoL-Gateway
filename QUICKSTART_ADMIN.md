# Quick Start - Admin Panel Setup

## Prerequisites

Ensure you have Python 3.7+ installed:
```bash
python3 --version
```

## Installation

### Step 1: Install Dependencies

```bash
# Install required Python packages
pip3 install --user flask pyotp qrcode pillow

# Or use requirements file
pip3 install --user -r requirements.txt
```

### Step 2: Run Setup Script

```bash
python3 setup_wol.py
```

During setup, you'll be asked:

1. **Configuration Method**: Choose option 2 for Web Admin Panel
2. **Admin Username**: Enter username (default: admin)
3. **Admin Password**: Enter a secure password (min 6 characters)
4. **Enable 2FA**: Optional, can be set up later

### Step 3: Configure at Least One Server

You'll need to configure at least one server during initial setup:
- Server Name (e.g., "Main Server")
- MAC Address (e.g., 00:11:22:33:44:55)
- Broadcast Address (default: 255.255.255.255)
- Site URL (e.g., http://192.168.1.100:8080)
- Wait Time (seconds to wait before redirect)

### Step 4: Start the Gateway

```bash
# Direct installation
./start.sh
# or
sudo python3 wol_gatway.py

# Docker (if using Docker)
cd .docker && docker compose up -d
```

### Step 5: Access Admin Panel

Open your browser and navigate to:
```
http://<server-ip>:<port>/admin
```

For example:
```
http://localhost:5000/admin
http://192.168.1.100:5000/admin
```

## First Login

1. Enter your admin username
2. Enter your password
3. If 2FA is enabled, enter the 6-digit code from your authenticator app

## Managing Servers

### Add a Server
1. Click "➕ Add New Server"
2. Fill in server details
3. Click "💾 Save Server"
4. **Restart the application**

### Edit a Server
1. Click "Edit" button next to server
2. Modify details
3. Click "💾 Save Server"
4. **Restart the application**

### Delete a Server
1. Click "Delete" button next to server
2. Confirm deletion
3. **Restart the application**

## Setting Up 2FA (Optional)

### Requirements
- Authenticator app on your phone:
  - Google Authenticator
  - Microsoft Authenticator
  - Authy
  - Any TOTP app

### Setup Steps
1. Log in to admin panel
2. Click "🔐 Security"
3. Click "Enable 2FA"
4. Scan QR code with your authenticator app
5. Enter 6-digit code to verify
6. **Save the secret code** in a secure location (for backup)

## Troubleshooting

### Cannot Access Admin Panel

**Problem**: `/admin` returns 403 Forbidden

**Solution**:
```bash
# Check if admin is enabled
cat admin_config.json

# If admin_enabled is false, run setup again
python3 setup_wol.py
```

### Forgot Password

**Solution**:
```bash
# Stop the application
sudo pkill -f wol_gatway.py

# Run setup to reset password
python3 setup_wol.py

# Choose admin panel option
# Set new password

# Start application again
./start.sh
```

### Lost 2FA Device

**Solution 1** (If you have the secret):
- Install authenticator app on new device
- Manually enter the secret code
- Use new device for 2FA

**Solution 2** (No backup):
```bash
# Edit admin_config.json
nano admin_config.json

# Set these values:
"2fa_enabled": false,
"2fa_secret": ""

# Save and restart application
```

### Import Errors

**Problem**: `ModuleNotFoundError: No module named 'pyotp'`

**Solution**:
```bash
pip3 install --user pyotp qrcode pillow
```

## Restart Application

After making changes in the admin panel:

### Direct Installation
```bash
# Find and stop the process
sudo pkill -f wol_gatway.py

# Start again
sudo python3 wol_gatway.py
```

### Docker
```bash
cd .docker
docker compose restart
```

### Using systemd (if configured)
```bash
sudo systemctl restart wol-gateway
```

## Security Tips

1. **Use Strong Passwords**: At least 12 characters with mixed case, numbers, symbols
2. **Enable 2FA**: Adds significant protection
3. **Backup Secret**: Save 2FA secret in password manager
4. **Regular Updates**: Keep dependencies updated
5. **HTTPS**: Use reverse proxy with SSL for production
6. **Firewall**: Restrict admin panel access to trusted networks

## Quick Reference

| Action | URL |
|--------|-----|
| Main Page | http://server:port/ |
| Admin Login | http://server:port/admin |
| Dashboard | http://server:port/admin/ |
| Security Settings | http://server:port/admin/security |
| Wake Server 0 | http://server:port/wake/0 |
| Wake Server 1 | http://server:port/wake/1 |

## Need Help?

1. Check `README_ADMIN.md` for detailed documentation
2. Review application logs
3. Verify configuration files are correct
4. Check GitHub issues

---

**Last Updated**: January 15, 2026
