# Admin Panel Documentation

## Overview

The WOL Gateway Admin Panel is a web-based interface for managing your Wake-on-LAN server configurations. It provides a secure, password-protected interface with optional two-factor authentication (2FA).

## Features

- 🔐 **Secure Authentication**: Password-protected access with bcrypt hashing
- 🔑 **Two-Factor Authentication**: Optional TOTP-based 2FA using authenticator apps
- ➕ **Server Management**: Add, edit, and delete server configurations
- 🔧 **Easy Configuration**: Manage all settings through a web interface
- 🚫 **Port Protection**: Flask port cannot be changed (requires restart)

## Initial Setup

### Option 1: During Setup Script

When running `setup_wol.py`, you'll be prompted to choose between:
1. **Setup Script** (Traditional) - Configure everything immediately
2. **Web Admin Panel** (Recommended) - Configure through browser interface

Choose option 2 for admin panel, then:
1. Enter an admin username (default: admin)
2. Create a password (minimum 6 characters)
3. Optionally enable 2FA (can be configured later)

### Option 2: Manual Configuration

Edit `admin_config.json`:
```json
{
    "admin_enabled": true,
    "admin_username": "admin",
    "admin_password_hash": "<hashed_password>",
    "2fa_enabled": false,
    "2fa_secret": ""
}
```

To generate a password hash in Python:
```python
import hashlib
password = "your_password"
hash = hashlib.sha256(password.encode()).hexdigest()
print(hash)
```

## Accessing the Admin Panel

1. Start the WOL Gateway: `./start.sh` or `sudo python3 wol_gatway.py`
2. Open browser: `http://<server-ip>:<port>/admin`
3. Log in with your credentials
4. If 2FA is enabled, enter your 6-digit code from authenticator app

## Managing Servers

### Add New Server
1. Click "➕ Add New Server" button
2. Fill in the form:
   - **Server Name**: Friendly name (e.g., "Main Server")
   - **MAC Address**: Format: XX:XX:XX:XX:XX:XX
   - **Broadcast Address**: Usually 255.255.255.255
   - **Site URL**: Where to redirect after wake
   - **Wait Time**: Seconds to wait before redirect
3. Click "💾 Save Server"
4. **Restart the application** for changes to take effect

### Edit Server
1. Click "Edit" button next to server
2. Modify fields as needed
3. Click "💾 Save Server"
4. **Restart the application** for changes to take effect

### Delete Server
1. Click "Delete" button next to server
2. Confirm deletion
3. **Restart the application** for changes to take effect

## Security Settings

### Change Password
1. Navigate to "🔐 Security" from dashboard
2. Enter current password
3. Enter new password (minimum 6 characters)
4. Confirm new password
5. Click "Update Password"

### Enable Two-Factor Authentication

#### Prerequisites
Install an authenticator app on your phone:
- Google Authenticator (iOS/Android)
- Microsoft Authenticator (iOS/Android)
- Authy (iOS/Android/Desktop)
- Any TOTP-compatible app

#### Setup Steps
1. Go to Security Settings
2. Click "Enable 2FA"
3. Scan the QR code with your authenticator app
   - Or manually enter the secret code
4. Enter the 6-digit code from your app
5. Click "✓ Verify and Enable 2FA"

#### Backup Your Secret
- Save the secret code in a secure location
- If you lose your phone, you'll need this to recover access
- Consider printing it and storing it securely

### Disable Two-Factor Authentication
1. Go to Security Settings
2. Enter your password
3. Click "Disable 2FA"

## Important Notes

### Configuration Changes
⚠️ **Changes require restart**: After adding, editing, or deleting servers, you must restart the WOL Gateway application for changes to take effect.

```bash
# Direct installation
sudo pkill -f wol_gatway.py
sudo python3 wol_gatway.py

# Docker
cd .docker && docker compose restart
```

### Flask Port
🔒 **Port cannot be changed**: The Flask port is locked and cannot be modified from the admin panel. To change the port:
1. Stop the application
2. Run `setup_wol.py` again
3. Configure the new port
4. Restart the application

### Session Management
- Sessions expire after closing browser
- Use "Remember Me" functionality (if implemented)
- Log out when finished for security

## Troubleshooting

### Cannot Access Admin Panel
**Symptom**: `/admin` returns 403 Forbidden

**Solution**: 
1. Check `admin_config.json` - ensure `admin_enabled: true`
2. Run `setup_wol.py` and enable admin panel
3. Restart the application

### Forgot Password
**Solution**:
1. Stop the application
2. Run `setup_wol.py`
3. Choose admin panel configuration
4. Set a new password
5. Restart the application

### Lost 2FA Device
**Solution 1** (If you have the secret):
1. Install authenticator app on new device
2. Manually enter the secret code from backup
3. Use the new device for 2FA codes

**Solution 2** (No backup):
1. Stop the application
2. Edit `admin_config.json`:
   ```json
   "2fa_enabled": false,
   "2fa_secret": ""
   ```
3. Restart application
4. Log in with password only
5. Re-enable 2FA with new device

### 2FA Code Not Working
**Possible causes**:
- Time sync issue: Ensure phone/device time is accurate
- Code expired: TOTP codes change every 30 seconds
- Wrong secret: Verify you're using correct authenticator entry

**Solutions**:
- Enable automatic time sync on your device
- Try entering the next code that appears
- Re-scan QR code if recently set up

### Admin Panel Not Loading
**Checklist**:
1. Verify application is running: `ps aux | grep wol_gatway`
2. Check logs for errors
3. Ensure port is accessible: `netstat -an | grep <port>`
4. Check firewall rules
5. Verify `admin_panel.py` exists in application directory

### Dependencies Missing
**Symptom**: Import errors or module not found

**Solution**:
```bash
pip3 install --user flask pyotp qrcode pillow
```

Or install from requirements file:
```bash
pip3 install --user -r requirements.txt
```

## API Endpoints

### Public Endpoints
- `/` - Main server selection page
- `/wake/<server_id>` - Trigger WOL for server

### Admin Endpoints (Authentication Required)
- `/admin/login` - Login page
- `/admin/logout` - Logout
- `/admin/` - Dashboard
- `/admin/server/add` - Add server form
- `/admin/server/edit/<id>` - Edit server form
- `/admin/server/delete/<id>` - Delete server (POST)
- `/admin/security` - Security settings

## File Structure

```
serverscripts/
├── wol_gatway.py          # Main Flask application
├── admin_panel.py         # Admin panel module
├── setup_wol.py           # Setup script
├── WOL_Brige.config       # Server configuration
├── admin_config.json      # Admin credentials & settings
├── requirements.txt       # Python dependencies
└── README_ADMIN.md        # This file
```

## Security Best Practices

1. **Strong Passwords**: Use at least 12 characters with mix of upper, lower, numbers, symbols
2. **Enable 2FA**: Adds significant security layer
3. **HTTPS**: Use reverse proxy (nginx/Apache) with SSL certificate for production
4. **Network Access**: Restrict admin panel access via firewall
5. **Regular Updates**: Keep dependencies updated
6. **Backup**: Regularly backup `admin_config.json` (securely)
7. **Logout**: Always logout when finished
8. **Monitor**: Review access logs regularly

## Advanced Configuration

### Reverse Proxy Setup (nginx)
```nginx
server {
    listen 80;
    server_name wol.example.com;
    
    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
    
    # Restrict admin access to internal network
    location /admin {
        allow 192.168.1.0/24;
        deny all;
        proxy_pass http://localhost:5000;
    }
}
```

### Docker Volume Mounting
Persist configuration across container rebuilds:
```yaml
services:
  wol-gateway:
    volumes:
      - ./config:/app/config
      - ./WOL_Brige.config:/app/WOL_Brige.config
      - ./admin_config.json:/app/admin_config.json
```

## Support

For issues or questions:
1. Check this documentation
2. Review application logs
3. Check GitHub issues
4. Submit new issue with details

---

**Version**: 2.0.0  
**Last Updated**: January 2026
