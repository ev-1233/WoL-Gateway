# Vagrant Testing Environment for WOL Gateway

## Setup Complete! ✅

Vagrant 2.3.4 with libvirt support has been installed on your system.

##  Usage Instructions

### 1. Start the VM
```bash
cd /home/ev/Documents/serverscripts
vagrant up
```

This will:
- Download Ubuntu 24.04 LTS (first run only)
- Create a VM with 2GB RAM and 2 CPUs
- Install Python 3, pip, and git
- Sync your workspace to `/vagrant` in the VM
- Forward port 5000 for Flask

### 2. SSH into the VM
```bash
vagrant ssh
```

### 3. Set Up and Test the Admin Panel

Inside the VM:
```bash
cd /vagrant

# Run the setup script
python3 setup_wol.py
# Choose option 2 for "Web Admin Panel"
# Set your admin username and password
# Optionally enable 2FA

# Start the WOL Gateway with sudo (for port binding)
sudo python3 wol_gatway.py
```

### 4. Access the Admin Panel

From your host machine browser:
```
http://localhost:5000/admin
```

Log in with the credentials you set up in step 3.

## Common Vagrant Commands

- `vagrant up` - Start the VM
- `vagrant halt` - Stop the VM
- `vagrant destroy` - Delete the VM (keeps Vagrantfile)
- `vagrant ssh` - Connect to the VM via SSH
- `vagrant reload` - Restart the VM (useful after config changes)
- `vagrant status` - Check VM status
- `vagrant reload --provision` - Restart and re-run provisioning script

## Troubleshooting

### "libvirt group" error
Log out and back in to refresh group permissions:
```bash
sudo usermod -aG libvirt $USER
# Then log out and log back in
```

### Check libvirt is running
```bash
sudo systemctl status virtqemud
```

### VM won't start
```bash
# Check for existing VMs
vagrant global-status

# Force clean up
vagrant destroy -f
vagrant up
```

### Port 5000 already in use
Stop any existing Flask apps on port 5000, or edit the Vagrantfile to use a different port.

## Benefits Over Multipass

- **Native to Red Hat ecosystem** - Better integration with Fedora
- **More reliable** - No timeouts or stuck states
- **Better documented** - Mature tooling with extensive community support
- **Declarative configuration** - Vagrantfile makes setup reproducible
- **Multiple providers** - Can switch to VirtualBox if needed

## Files Created

- [Vagrantfile](./Vagrantfile) - VM configuration
- [VAGRANT_SETUP.md](./VAGRANT_SETUP.md) - This file
