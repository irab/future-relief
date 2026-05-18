#!/bin/bash
# QGIS Installation Script for Debian
# This script installs QGIS from Debian repositories

set -e

echo "========================================="
echo "QGIS Installation Script"
echo "========================================="
echo ""

# Check if running as root
if [ "$EUID" -eq 0 ]; then 
    echo "Please do not run this script as root/sudo."
    echo "The script will prompt for sudo when needed."
    exit 1
fi

echo "Step 1: Updating package list..."
sudo apt-get update

echo ""
echo "Step 2: Installing QGIS from Debian repositories..."
echo "QGIS version available: $(apt-cache policy qgis | grep Candidate | awk '{print $2}')"
echo ""

sudo apt-get install -y qgis qgis-plugin-grass

echo ""
echo "========================================="
echo "Installation Complete!"
echo "========================================="
echo ""
echo "QGIS has been installed. You can now:"
echo "1. Launch QGIS from your applications menu, or"
echo "2. Run 'qgis' from the command line"
echo ""
echo "Next steps:"
echo "1. Open QGIS"
echo "2. Go to Plugins → Manage and Install Plugins"
echo "3. Search for 'DEMto3D' and install it"
echo ""
echo "For detailed instructions, see: docs/QGIS_STL_CONVERSION.md"
