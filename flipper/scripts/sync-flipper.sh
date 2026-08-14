#!/bin/bash
# Sync Flipper Zero based on flipper-config.yml
# Implements device polling to overcome port locks

CONFIG_FILE="flipper-config.yml"
CLI_PATH="C:/Program Files/qFlipper/qFlipper-cli.exe"

# Function to wait for device access
wait_for_device() {
    echo "Waiting for Flipper Zero on COM9..."
    while ! "$CLI_PATH" info > /dev/null 2>&1; do
        echo "Device busy or disconnected. Retrying in 5 seconds..."
        sleep 5
    done
    echo "Device detected!"
}

if [ ! -f "$CLI_PATH" ]; then
    echo "Error: qFlipper-cli not found at $CLI_PATH"
    exit 1
fi

# Run the wait-for-device loop
wait_for_device

echo "Syncing Flipper Zero with $CONFIG_FILE..."
# Backup
"$CLI_PATH" backup "flipper_backup_$(date +%Y%m%d_%H%M%S).qpf"
echo "Backup complete."

# Placeholder for app sync logic (to be added with ufbt)
echo "Pipeline: Ready for app sync logic."
