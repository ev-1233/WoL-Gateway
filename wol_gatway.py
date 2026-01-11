#!/usr/bin/env python3
"""
Wake-on-LAN (WOL) Gateway - Flask Web Application

This application provides a web-based Wake-on-LAN gateway that:
  1. Receives HTTP requests at the /wake endpoint
  2. Sends a WOL magic packet to wake up a remote server
  3. Displays a waiting page while the server boots
  4. Automatically redirects to the target site once boot time elapses

Requirements:
  - Flask: pip install flask
  - wakeonlan utility: pkg install wakeonlan (Termux) or apt install wakeonlan (Linux)
  - WOL_Brige.config file created by setup_wol.py

Usage:
  python wol_gatway.py
  
Then access: http://<server-ip>:<port>/wake
"""

import subprocess
import time
import json
import os
from flask import Flask, redirect, Response

# =================================================================
#                         USER CONFIGURATION
# =================================================================

# Configuration file path - must be created by setup_wol.py first
CONFIG_FILE = "WOL_Brige.config"

def load_config():
    """
    Loads and validates the configuration from WOL_Brige.config.
    
    This function:
      1. Checks if the config file exists
      2. Parses the JSON content
      3. Validates that all required keys are present
      4. Validates each configuration value
      5. Returns a dictionary with validated config values
    
    Returns:
        dict: Validated configuration with keys: WOL_MAC_ADDRESS, SITE_URL,
              WAIT_TIME_SECONDS, PORT
    
    Raises:
        FileNotFoundError: If config file doesn't exist
        ValueError: If config is invalid or missing required fields
    """
    # Define all required configuration keys
    required_keys = ("WOL_MAC_ADDRESS", "BROADCAST_ADDRESS", "SITE_URL", "WAIT_TIME_SECONDS", "PORT")

    # Check if configuration file exists
    if not os.path.exists(CONFIG_FILE):
        raise FileNotFoundError(
            f"Config file {CONFIG_FILE} is required. Run setup_wol.py to create it."
        )

    # Load and parse the JSON configuration file
    try:
        with open(CONFIG_FILE, 'r') as f:
            user_config = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Error parsing {CONFIG_FILE}: {e}") from e

    # Verify all required keys are present
    missing = [key for key in required_keys if key not in user_config]
    if missing:
        raise ValueError(f"Missing required config keys: {', '.join(missing)}")

    # Extract and validate MAC address
    mac = str(user_config["WOL_MAC_ADDRESS"]).strip()
    # Extract and validate broadcast address
    broadcast = str(user_config["BROADCAST_ADDRESS"]).strip()
    # Extract and validate site URL
    site = str(user_config["SITE_URL"]).strip()
    # Extract wait time (will validate as integer below)
    wait_raw = user_config["WAIT_TIME_SECONDS"]

    # Validate MAC address is not empty
    if not mac:
        raise ValueError("WOL_MAC_ADDRESS must be set in the config file.")
    
    # Validate broadcast address is not empty
    if not broadcast:
        raise ValueError("BROADCAST_ADDRESS must be set in the config file.")
    
    # Validate site URL is not empty
    if not site:
        raise ValueError("SITE_URL must be set in the config file.")

    # Validate and convert wait time to integer
    try:
        wait = int(wait_raw)
    except (TypeError, ValueError) as e:
        raise ValueError("WAIT_TIME_SECONDS must be an integer.") from e

    # Ensure wait time is positive
    if wait <= 0:
        raise ValueError("WAIT_TIME_SECONDS must be greater than zero.")

    # Extract and validate port number
    port_raw = user_config["PORT"]
    try:
        port = int(port_raw)
    except (TypeError, ValueError) as e:
        raise ValueError("PORT must be an integer.") from e

    # Ensure port is within valid range (1-65535)
    if port <= 0 or port > 65535:
        raise ValueError("PORT must be between 1 and 65535.")

    # Log successful configuration load with timestamp
    print(f"[{time.strftime('%H:%M:%S')}] Loaded config from {CONFIG_FILE}")

    # Return validated configuration dictionary
    return {
        "WOL_MAC_ADDRESS": mac,
        "BROADCAST_ADDRESS": broadcast,
        "SITE_URL": site,
        "WAIT_TIME_SECONDS": wait,
        "PORT": port,
    }

# Load configuration at startup - will exit with error if config is invalid
config = load_config()

# Extract configuration values into module-level constants for easy access

# 1. MAC Address of the Server's Network Card (e.g., "00:1A:2B:3C:4D:5E")
#    This is the hardware address of the network interface to wake
WOL_MAC_ADDRESS = config["WOL_MAC_ADDRESS"]

# 2. Broadcast Address for sending WOL packets (e.g., "255.255.255.255" or "192.168.1.255")
#    This determines where the magic packet will be broadcast on the network
BROADCAST_ADDRESS = config["BROADCAST_ADDRESS"]

# 3. The final URL of your site (e.g., "http://panel.yourdomain.com")
#    Users will be redirected here after the wait time elapses
SITE_URL = config["SITE_URL"]

# 4. Time (in seconds) to wait for the server to boot up
#    Should be long enough for the server to fully start and become accessible
WAIT_TIME_SECONDS = config["WAIT_TIME_SECONDS"]

# 5. Port for Flask to run on (e.g., 5000, 8080, 3000)
#    Remember to forward this port in your router if accessing externally
PORT = config["PORT"]

# =================================================================
#                     FLASK APPLICATION START
# =================================================================

# Initialize Flask application
app = Flask(__name__)

# =================================================================
#                    HTML WAITING PAGE TEMPLATE
# =================================================================
# This HTML page is displayed to users after triggering the WOL packet.
# Key features:
#   - Auto-refresh meta tag redirects to SITE_URL after WAIT_TIME_SECONDS
#   - CSS loading spinner animation for visual feedback
#   - Responsive design with centered container
#   - User-friendly messages explaining what's happening
WAITING_PAGE_HTML = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Server Starting...</title>
    <meta http-equiv="refresh" content="{WAIT_TIME_SECONDS};url={SITE_URL}">
    <style>
        body {{ font-family: sans-serif; text-align: center; margin-top: 50px; background-color: #f0f0f0; }}
        .container {{ background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); display: inline-block; }}
        h1 {{ color: #333; }}
        .loader {{ border: 8px solid #f3f3f3; border-top: 8px solid #3498db; border-radius: 50%; width: 50px; height: 50px; animation: spin 2s linear infinite; margin: 20px auto; }}
        @keyframes spin {{ 0% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(360deg); }} }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Starting Server...</h1>
        <div class="loader"></div>
        <p>Sending Wake-on-LAN signal. Please wait approximately <strong>{WAIT_TIME_SECONDS} seconds</strong>.</p>
        <p>You will be automatically redirected to your domain.</p>
        <p>If the page fails to load, the server may still be booting. Please try refreshing.</p>
    </div>
</body>
</html>
"""

def find_wakeonlan_command():
    """
    Finds the wakeonlan command in various possible locations.
    
    When running with sudo, the PATH may not include user's local bin directories,
    so we need to check multiple possible locations.
    
    Returns:
        str or None: Full path to wakeonlan command, or None if not found
    """
    # Possible locations for wakeonlan command
    possible_paths = [
        'wakeonlan',  # Try PATH first
        '/usr/bin/wakeonlan',
        '/usr/local/bin/wakeonlan',
        '/bin/wakeonlan',
    ]
    
    # Also check user's local bin (get the actual user even when running with sudo)
    if 'SUDO_USER' in os.environ:
        # Running with sudo, get the real user's home directory
        sudo_user = os.environ['SUDO_USER']
        user_local_bin = f'/home/{sudo_user}/.local/bin/wakeonlan'
        possible_paths.insert(1, user_local_bin)
    else:
        # Not running with sudo, check current user's local bin
        user_home = os.path.expanduser('~')
        user_local_bin = os.path.join(user_home, '.local', 'bin', 'wakeonlan')
        possible_paths.insert(1, user_local_bin)
    
    # Try each path
    for cmd_path in possible_paths:
        try:
            # Check if it's just a command name (try 'which')
            if '/' not in cmd_path:
                result = subprocess.run(['which', cmd_path], capture_output=True, text=True)
                if result.returncode == 0:
                    return cmd_path
            # Check if it's a full path that exists
            elif os.path.isfile(cmd_path) and os.access(cmd_path, os.X_OK):
                return cmd_path
        except Exception:
            continue
    
    return None

@app.route('/wake', methods=['GET'])
def wake_server_and_redirect():
    """
    Main endpoint that triggers Wake-on-LAN and displays the waiting page.
    
    When a user visits http://<server>:<port>/wake, this function:
      1. Sends a WOL magic packet to wake the sleeping server
      2. Returns an HTML page with auto-redirect after WAIT_TIME_SECONDS
    
    The magic packet is a special network message that tells the server's
    network card to power on the machine.
    
    Returns:
        Response: HTML waiting page (200) or error message (500)
    """
    
    # =================================================================
    # Step 1: Send the Wake-on-LAN Magic Packet
    # =================================================================
    # Find the wakeonlan command (may be in different locations)
    wakeonlan_cmd = find_wakeonlan_command()
    
    if not wakeonlan_cmd:
        error_message = "WOL Error: 'wakeonlan' command not found. Please install it:\n"
        error_message += "  Debian/Ubuntu: sudo apt-get install wakeonlan\n"
        error_message += "  Fedora/RHEL: sudo dnf install wol\n"
        error_message += "  Or via pip: pip3 install --user wakeonlan"
        print(f"[{time.strftime('%H:%M:%S')}] {error_message}")
        return error_message, 500
    
    # Uses the 'wakeonlan' command-line utility to send the magic packet
    try:
        # Execute: wakeonlan -i <BROADCAST_ADDRESS> <MAC_ADDRESS>
        # -i flag specifies the broadcast address to send the packet to
        # check=True: raises CalledProcessError if command fails
        # capture_output=True: captures stdout/stderr for error reporting
        subprocess.run([wakeonlan_cmd, '-i', BROADCAST_ADDRESS, WOL_MAC_ADDRESS], check=True, capture_output=True)
        print(f"[{time.strftime('%H:%M:%S')}] WOL Magic Packet sent to {WOL_MAC_ADDRESS} via {BROADCAST_ADDRESS} using {wakeonlan_cmd}")
    
    except subprocess.CalledProcessError as e:
        # Command executed but failed (non-zero exit code)
        # This could happen if MAC address format is invalid
        error_message = f"WOL Error: Could not send packet. Check MAC address: {e.stderr.decode()}"
        print(f"[{time.strftime('%H:%M:%S')}] {error_message}")
        return error_message, 500
    
    except Exception as e:
        # Any other error (shouldn't happen since we checked for command existence)
        error_message = f"WOL Error: Unexpected error: {str(e)}"
        print(f"[{time.strftime('%H:%M:%S')}] {error_message}")
        return error_message, 500

    # =================================================================
    # Step 2: Return the HTML Waiting Page
    # =================================================================
    # The HTML page contains a meta refresh tag that will automatically
    # redirect the user's browser to SITE_URL after WAIT_TIME_SECONDS
    return Response(WAITING_PAGE_HTML, mimetype='text/html')

@app.route('/')
def home():
    """
    Root endpoint - landing page with button to start the server.
    
    This is displayed when users visit http://<server>:<port>/
    It provides a button to wake the server, matching the design of the /wake page.
    
    Returns:
        Response: HTML landing page
    """
    
    landing_page_html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Server Gateway</title>
    <style>
        body {{ font-family: sans-serif; text-align: center; margin-top: 50px; background-color: #f0f0f0; }}
        .container {{ background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); display: inline-block; }}
        h1 {{ color: #333; }}
        .button {{ 
            background-color: #3498db; 
            color: white; 
            padding: 15px 32px; 
            text-align: center; 
            text-decoration: none; 
            display: inline-block; 
            font-size: 18px; 
            margin: 20px 2px; 
            cursor: pointer; 
            border: none; 
            border-radius: 5px;
            transition: background-color 0.3s;
        }}
        .button:hover {{ background-color: #2980b9; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🖥️ Server Gateway</h1>
        <p>Click the button below to start the server.</p>
        <a href="/wake" class="button">Start Server</a>
        <p style="color: #666; font-size: 14px; margin-top: 20px;">
            The server will be woken and you'll be redirected in approximately {WAIT_TIME_SECONDS} seconds.
        </p>
    </div>
</body>
</html>
    """
    
    return Response(landing_page_html, mimetype='text/html')

# =================================================================
#                     APPLICATION ENTRY POINT
# =================================================================
if __name__ == '__main__':
    # Start the Flask development server
    # host='0.0.0.0' - Binds to all network interfaces (allows external connections)
    #                  Change to '127.0.0.1' if only local access is needed
    # port=PORT - Uses the port specified in the config file
    # debug=False - Disables debug mode for production use
    #               Set to True during development for auto-reload and detailed errors
    
    print(f"[{time.strftime('%H:%M:%S')}] Flask App starting on http://0.0.0.0:{PORT}")
    print(f"[{time.strftime('%H:%M:%S')}] Waking MAC: {WOL_MAC_ADDRESS} via Broadcast: {BROADCAST_ADDRESS}")
    print(f"[{time.strftime('%H:%M:%S')}] Redirect URL: {SITE_URL}")
    print(f"[{time.strftime('%H:%M:%S')}] Access the /wake endpoint to trigger WOL")
    
    app.run(host='0.0.0.0', port=PORT, debug=False)