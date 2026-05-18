# Installing QGIS and DEMto3D Plugin

This guide will help you install QGIS and the DEMto3D plugin on Debian Linux.

## Quick Installation

Run the installation script:

```bash
cd /home/x/repos/future-relief
./scripts/install_qgis.sh
```

The script will:
1. Add the official QGIS repository
2. Install QGIS and required dependencies
3. Guide you through the next steps

## Manual Installation

If you prefer to install manually:

### Step 1: Add QGIS Repository

```bash
# Update package list
sudo apt-get update

# Install prerequisites
sudo apt-get install -y gnupg software-properties-common

# Add QGIS GPG key
wget -qO - https://qgis.org/downloads/qgis-2024.gpg.key | sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/qgis-archive.gpg

# Add QGIS repository (for Debian Trixie)
echo "deb https://qgis.org/debian trixie main" | sudo tee /etc/apt/sources.list.d/qgis.list

# Update package list again
sudo apt-get update
```

### Step 2: Install QGIS

```bash
sudo apt-get install -y qgis qgis-plugin-grass
```

### Step 3: Verify Installation

```bash
qgis --version
```

You should see the QGIS version number.

## Installing DEMto3D Plugin

After QGIS is installed:

1. **Launch QGIS**
   - From applications menu, or
   - Run `qgis` from terminal

2. **Open Plugin Manager**
   - Go to **Plugins** → **Manage and Install Plugins**
   - Or press `Ctrl+Shift+P`

3. **Install DEMto3D**
   - Click on **All** tab
   - Search for "**DEMto3D**"
   - Select **DEMto3D** from the list
   - Click **Install Plugin**
   - Wait for installation to complete

4. **Verify Installation**
   - Go to **Raster** menu
   - You should see **DEMto3D** option
   - If not, go to **Plugins** → **Manage and Install Plugins** → **Installed** tab
   - Make sure DEMto3D is checked/enabled

## Alternative: Install from Debian Repositories

If you prefer to use Debian's default repositories (may have older version):

```bash
sudo apt-get update
sudo apt-get install -y qgis
```

Note: The Debian repositories may have an older version of QGIS. The official QGIS repository (method above) provides the latest stable version.

## Troubleshooting

### QGIS won't start
- Check if all dependencies are installed: `sudo apt-get install -f`
- Try running from terminal to see error messages: `qgis`

### Plugin not appearing
- Make sure plugin is enabled in Plugin Manager → Installed tab
- Restart QGIS after installation
- Check QGIS version compatibility (DEMto3D works with QGIS 3.x)

### Repository errors
- If repository key fails, try:
  ```bash
  sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-key 51F523511C7028C3
  ```

### Permission errors
- Make sure you have sudo access
- Some operations may require user permissions for plugin directory

## Next Steps

Once QGIS and DEMto3D are installed, see:
- [QGIS_STL_CONVERSION.md](QGIS_STL_CONVERSION.md) for converting your DEM to STL

## System Requirements

- **RAM**: 4GB minimum, 8GB+ recommended
- **Disk Space**: ~2GB for QGIS installation
- **Graphics**: OpenGL support recommended for 3D features
- **OS**: Debian 11+ (Bullseye/Trixie)
