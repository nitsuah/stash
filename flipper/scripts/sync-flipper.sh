#!/bin/bash
# Sync Flipper Zero based on flipper-config.yml
# Automates preparation of FAP files for Flipper Lab deployment

CONFIG_FILE="flipper-config.yml"
CLI_PATH="C:/Program Files/qFlipper/qFlipper-cli.exe"
APPS_DIR="./flipper/apps/bin"

if [ ! -f "$CLI_PATH" ]; then
    echo "Error: qFlipper-cli not found at $CLI_PATH"
    exit 1
fi

echo "--- Flipper Pipeline Active ---"
echo "Binary Apps Found in $APPS_DIR:"
ls -l "$APPS_DIR"

# Perform Backup
echo "Performing Flipper Backup..."
"$CLI_PATH" backup "flipper_backup_$(date +%Y%m%d_%H%M%S).qpf"

echo "Sync pipeline complete: FAPs are staged in flipper/apps/bin for Flipper Lab deployment."
