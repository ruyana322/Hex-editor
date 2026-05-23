#!/bin/bash
# Setup script untuk Hex Editor Termux Tool

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  HEX EDITOR - Video Binary Analysis Tool Setup                 ║"
echo "║                by D4nzxml                                      ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Check jika running di Termux
if [ ! -d "$PREFIX" ]; then
    echo "❌ This setup script is designed for Termux!"
    echo "   Install Termux from: https://termux.com"
    exit 1
fi

echo "📦 Installing dependencies..."
echo ""

# Update packages
pkg update -y
pkg upgrade -y

# Install required packages
echo "⏳ Installing Python dan tools..."
pkg install -y python
pkg install -y ffmpeg
pkg install -y git

# Verify installation
echo ""
echo "✓ Checking installations..."
python3 --version
ffmpeg -version 2>/dev/null | head -1

echo ""
echo "✓ Setting up hex_editor tool..."

# Create tool directory
TOOL_DIR="$HOME/.local/bin"
mkdir -p "$TOOL_DIR"

# Copy main script
cp hex_editor_tool.py "$TOOL_DIR/hex_editor"
chmod +x "$TOOL_DIR/hex_editor"

# Add PATH jika belum ada
if ! grep -q "\$HOME/.local/bin" ~/.bashrc 2>/dev/null; then
    echo 'export PATH="$PATH:$HOME/.local/bin"' >> ~/.bashrc
fi

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                    ✓ SETUP COMPLETE!                          ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "🚀 How to use:"
echo "   1. Reload shell: source ~/.bashrc"
echo "   2. Run tool:     hex_editor"
echo "   3. Or run with:  python3 hex_editor_tool.py"
echo ""
echo "📝 Features:"
echo "   ✓ File Browser"
echo "   ✓ Video Structure Scanner"
echo "   ✓ Hex Viewer/Editor"
echo "   ✓ Metadata Analyzer"
echo "   ✓ Corruption Checker"
echo "   ✓ Report Generator"
echo ""
echo "By D4nzxml 👨‍💻"
echo ""
