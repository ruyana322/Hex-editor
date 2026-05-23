# HEX EDITOR - Video Binary Analysis Tool
## by D4nzxml

```
╔════════════════════════════════════════════════════════════════╗
║           HEX EDITOR - Video Binary Analysis Tool              ║
║                     by D4nzxml                                 ║
╚════════════════════════════════════════════════════════════════╝
```

### 📋 Deskripsi
Hex Editor adalah tool terminal untuk menganalisis dan mengedit file binary, khususnya video files. Didesain khusus untuk Termux, tool ini memberikan pengalaman yang ringan dan responsif dibanding GUI hex editor biasa.

### ✨ Fitur Utama

#### 1. **📂 File Browser**
- Browse file system dengan interface yang user-friendly
- Support untuk navigasi folder
- Display ukuran file

#### 2. **🔍 Scan Struktur Video**
- Deteksi format video otomatis (MP4, MOV, WebM, MKV, dll)
- Scan MP4/MOV box structure
- Identify critical boxes (ftyp, moov, mdat)
- Hash calculation (MD5 & SHA256)

#### 3. **🔧 Repair Video**
- Attempt automatic MP4 repair menggunakan ffmpeg
- Rebuild corrupted moov box
- Create backup sebelum modify

#### 4. **📊 Analyzer Metadata**
- Extract file metadata
- Parse MP4 atom structure
- Display format information
- Show file timestamps

#### 5. **⚡ Faststar Optimizer** (Coming Soon)
- Optimize file size
- Remove redundant data
- Streaming-optimized output

#### 6. **⚠️  Check Corruption**
- Detect missing critical boxes
- Identify null byte corruption
- Check file integrity
- Report potential issues

#### 7. **📝 Export Report**
- Generate JSON report
- Save analysis results
- Track file history
- Timestamp all changes

#### 8. **✏️  Edit Write File Biner**
- Full hex editor dengan ASCII display
- **Search functionality:**
  - Search hex bytes (e.g., `FF D8 FF`)
  - Search ASCII strings
  - Display semua hasil
- **Write bytes** pada specific offset
- **Save changes** dengan automatic backup

---

## 🚀 Instalasi

### Requirements
- Termux (Android)
- Python 3.8+
- ffmpeg (optional, untuk repair)
- ~50MB free space

### Quick Install

```bash
# 1. Download script
git clone https://github.com/yourusername/hex-editor.git
cd hex-editor

# 2. Run setup
bash setup.sh

# 3. Reload shell
source ~/.bashrc

# 4. Run tool
hex_editor
```

### Manual Install

```bash
# Update packages
pkg update && pkg upgrade

# Install dependencies
pkg install -y python ffmpeg git

# Copy script
python3 hex_editor_tool.py
```

---

## 📖 Panduan Penggunaan

### Main Menu
```
[1] 📂 Browse & Select File    - Pilih file yang akan dianalisis
[2] 🔍 Scan Struktur Video     - Lihat struktur internal video
[3] 🔧 Repair Video            - Coba repair file yang rusak
[4] 📊 Analyzer Metadata       - Analisis metadata detail
[5] ⚡ Faststar Optimizer      - Optimize file (coming soon)
[6] ⚠️  Check Corruption        - Cek corruption
[7] 📝 Export Report           - Simpan hasil analisis
[8] ✏️  Edit Write File Biner   - Edit hex langsung
[0] Exit                        - Keluar
```

### Contoh Workflow

#### Scan & Repair Corrupted MP4
```
1. Pilih [1] - Browse file
2. Select file video yang rusak
3. Pilih [2] - Scan struktur
4. Lihat error/issue yang terdeteksi
5. Pilih [3] - Repair video
6. Check hasil di file_repaired.mp4
```

#### Analyze Video Metadata
```
1. Pilih [1] - Browse file
2. Select file
3. Pilih [4] - Analyzer metadata
4. View detailed metadata
7. Pilih [7] - Export report untuk simpan hasil
```

#### Edit Hex Manual
```
1. Pilih [1] - Browse file
2. Select file
3. Pilih [8] - Edit/Write
4. View hex editor
5. Pilih [1] - Search (cari specific byte/string)
6. Pilih [2] - Write bytes (edit pada offset tertentu)
7. Pilih [4] - Save changes
```

---

## 🔬 Technical Details

### Format Support
- **MP4** - ftyp signature detection, atom parsing
- **MOV** - QuickTime format support
- **MKV/WebM** - EBML format detection
- **MP3** - ID3 tag detection
- **AVI/WAV** - RIFF format

### Scan Capabilities
- Magic byte detection
- Atom/box structure analysis
- Hash verification (MD5, SHA256)
- Corruption pattern detection
- Metadata extraction

### Limitations
- Large files (>500MB) display limited scan
- Some proprietary formats not supported
- Repair limited to basic MP4 rebuilding
- No video transcoding (use ffmpeg separately)

---

## 🛠️ Advanced Usage

### Search Hex
```
Search Term Examples:
- "FF D8 FF E0" (hex bytes)
- "ftyp" (ASCII string)
- "00 00 00 20" (with spaces)
```

### Write Bytes
```
Offset: 00000100
Data: FF D8 FF E0 00 10 4A 46 49 46

Akan write 10 bytes pada offset 0x100
```

### Output Files
```
file.mp4                    - Original file
file.mp4.backup             - Backup sebelum edit
file.mp4_repaired.mp4       - Hasil repair
file.mp4_report.json        - Analysis report
```

---

## 📊 Report Format

Generated JSON report:
```json
{
  "generated_at": "2024-01-15T10:30:00",
  "tool_version": "1.0.0",
  "author": "D4nzxml",
  "analysis": {
    "file_info": {
      "path": "/path/to/file.mp4",
      "filename": "file.mp4",
      "size": 1048576,
      "size_human": "1.00 MB",
      "modified": "2024-01-15T10:00:00",
      "md5": "abc123...",
      "sha256": "def456...",
      "detected_format": "MP4 (ISOM)"
    },
    "headers": [...],
    "errors": [...]
  }
}
```

---

## ⚙️ Settings & Configuration

### Environment Variables
```bash
# Disable backups
export HEX_NO_BACKUP=1

# Custom temp directory
export HEX_TEMP=/path/to/temp
```

### Configuration File (~/.config/hex_editor/config)
```ini
# Backup on save
backup_on_save=true

# Max file size for full scan (in MB)
max_scan_size=500

# Enable debug mode
debug=false
```

---

## 🐛 Troubleshooting

### "ffmpeg not found"
```bash
# Install ffmpeg
pkg install ffmpeg
```

### "Permission denied" saat write
```bash
# Check file permissions
ls -la /path/to/file

# Repair dengan root (jika diperlukan)
# Tapi generally jangan gunakan root untuk safety
```

### Large file hang
```bash
# Tool auto-limit scan untuk file besar (>500MB)
# Untuk files ini, manual hex edit terbatas pada first 1MB view
# Split file jika perlu:
split -b 100M largefile.bin part_
```

### Search tidak menemukan hasil
```bash
# Verify search term format
# Hex: gunakan spacing atau tanpa spacing (keduanya OK)
# String: case-sensitive

# Contoh yang bekerja:
"FF D8 FF"     ✓
"FFD8FF"       ✓
"hello"        ✓ (case-sensitive)
```

---

## 📚 Resources

### Useful Tools to Install
```bash
# View raw file bytes
pkg install hexdump

# Video analysis
pkg install mediainfo

# Binary comparison
pkg install diffutils
```

### Combined Usage
```bash
# Scan dengan mediainfo
mediainfo video.mp4

# Compare 2 files
hexdump -C file1.bin | head -100
hexdump -C file2.bin | head -100

# Extract section dari file
dd if=largefile.bin of=extracted.bin bs=1 skip=1000 count=512
```

---

## 📝 Changelog

### v1.0.0 (Initial Release)
- ✓ File browser
- ✓ Video structure scanner
- ✓ Hex viewer/editor
- ✓ Corruption checker
- ✓ Metadata analyzer
- ✓ Report generator
- ✓ Basic repair functionality

### v1.1.0 (Planned)
- [ ] Faststar optimizer
- [ ] Batch processing
- [ ] Custom plugins
- [ ] Video stream analysis
- [ ] Advanced repair

---

## 🤝 Contributing

Issues & suggestions? Create an issue atau contact:
- **Author:** D4nzxml
- **Project:** Hex Editor Termux Tool

---

## ⚖️ Legal

Hex Editor tool ini didesain untuk **legitimate purposes only**:
- ✓ Analyze your own files
- ✓ Recover corrupted data
- ✓ Educational purposes
- ✓ Software development & debugging

**Dilarang** untuk:
- ✗ Bypass copyright protection
- ✗ Unauthorized access
- ✗ Illegal activities

---

## 📄 License

This tool is provided as-is for personal/educational use.

---

## Tips & Tricks

### 1. Always Backup
```bash
# Script auto-backup, tapi manual backup juga safe
cp important_file.mp4 important_file.mp4.original
```

### 2. Understand File Format
```bash
# Belajar struktur MP4:
# - ftyp (file type)
# - mdat (media data)
# - moov (metadata)
# - free (padding)

# Edit hanya jika tahu apa yang dilakukan!
```

### 3. Use Search Effectively
```bash
# Find all instances dari specific box
Search: "6D 6F 6F 76"  (hex untuk 'moov')

# Find string
Search: "copyright"
```

### 4. Combine with Other Tools
```bash
# Get file info
file video.mp4

# See first 1KB
head -c 1024 video.mp4 | od -x

# Count specific bytes
grep -ao "FF" video.mp4 | wc -l
```

---

**Created with ❤️ by D4nzxml**

```
╔════════════════════════════════════════════════════════════════╗
║             Happy Analyzing & Editing! 👨‍💻                    ║
╚════════════════════════════════════════════════════════════════╝
```
