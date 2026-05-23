# QUICK START GUIDE - Hex Editor Termux Tool

## 🚀 Instalasi 5 Menit

### Step 1: Persiapan
```bash
# Buka Termux
# Copy-paste command berikut:

pkg update && pkg upgrade -y
pkg install -y python ffmpeg git
```

### Step 2: Download & Setup
```bash
# Clone atau copy files
mkdir -p ~/hex-editor
cd ~/hex-editor

# Copy hex_editor_tool.py ke folder ini
# (atau git clone dari repo)

chmod +x *.py
```

### Step 3: Jalankan
```bash
python3 hex_editor_tool.py
```

---

## 📱 Cara Pemakaian

### Skenario 1: Cek Video yang Rusak
```
1. Jalankan: python3 hex_editor_tool.py
2. Menu utama muncul
3. Tekan: 1 (Browse file)
4. Cari video.mp4 yang rusak
5. Tekan Enter
6. Kembali ke menu, tekan: 2 (Scan)
7. Lihat info & error yang terdeteksi
8. Tekan: 6 (Check Corruption)
9. Tekan: 7 (Export report)
✓ Report tersimpan di video.mp4_report.json
```

### Skenario 2: Edit Hex Langsung
```
1. Pilih file [1]
2. Tekan [8] Edit/Write
3. View hex display
4. Tekan [1] Search
5. Cari: "00 00 00"
6. Tekan [2] Write
7. Offset: 00000100
8. Data: FF FF FF FF
9. Tekan [4] Save
10. Backup otomatis dibuat ✓
```

### Skenario 3: Repair Rusak MP4
```
1. Select file [1]
2. Tekan [3] Repair
3. Tool cek ffmpeg tersedia
4. Proses repair otomatis
5. Hasil: file_repaired.mp4 ✓
```

---

## 🎮 Kontrol Keyboard

### Main Menu
- **1-8** : Pilih fitur
- **0** : Exit
- **Enter** : Confirm

### File Browser
- **[..] atau .. enter** : Naik ke parent folder
- **1-9** : Pilih file/folder
- **0** : Back

### Hex Editor
- **1** : Search hex/string
- **2** : Write bytes
- **3** : Next page
- **4** : Save
- **0** : Back

---

## 💡 Tips Praktis

### Tip 1: Backup Penting
```bash
# Tool auto-backup, tapi untuk aman:
cp video.mp4 video.mp4.original
```

### Tip 2: Understand Hex Values
```
Common values:
00 = null byte
FF = 255 (max byte)
0A = line feed (\n)
0D = carriage return (\r)

MP4 boxes:
"66 74 79 70" = "ftyp"
"6D 6F 6F 76" = "moov"
"6D 64 61 74" = "mdat"
```

### Tip 3: Search Pattern
```bash
# Cari di hex editor:
"FF D8 FF" - JPEG header
"00 00 00 18 66 74 79 70" - MP4 ftyp box
"49 44 33" - MP3 ID3 tag
```

### Tip 4: Termux Performance
```bash
# Tool ringan & fast, tapi jika lambat:

# Check available memory
free -h

# Close other apps
ps aux | grep -v grep | wc -l

# Kill unused procs
killall app_name  # hati-hati
```

---

## 📊 Output Examples

### Scan Hasil Output
```
═══ SCAN HASIL ═══

File Info:
  path: /storage/emulated/0/video.mp4
  filename: video.mp4
  size: 52428800
  size_human: 50.00 MB
  modified: 2024-01-15T10:30:45
  md5: abc123def456...
  sha256: xyz789...
  detected_format: MP4 (ISOM)

Boxes Found:
  ftyp @ 00000000 (32.00 B)
  mdat @ 00000020 (49.99 MB)
  moov @ 03C00020 (100.00 KB)

Issues Detected:
  ⚠️  No critical issues found
```

### Hex Editor Display
```
Offset      Hex Data                              ASCII
────────────────────────────────────────────────────────
00000000    00 00 00 20 66 74 79 70 69 73 6f 6d   .... ftypiso...
00000010    00 00 00 00 69 73 6f 6d 69 73 6f 32   ....isomiso2....
00000020    6d 70 34 31 6d 70 34 32 00 00 00 08   mp41mp42........
```

---

## ❌ Troubleshooting

### Problem: "Permission Denied"
```bash
# Fix 1: Change permissions
chmod 755 hex_editor_tool.py

# Fix 2: Check file owner
ls -la file.mp4

# Fix 3: Copy to writable location
cp /read-only/file.mp4 ~/file.mp4
python3 hex_editor_tool.py
```

### Problem: "ffmpeg not found"
```bash
# Install ffmpeg
pkg install ffmpeg

# Verify
which ffmpeg
ffmpeg -version
```

### Problem: "File too large"
```bash
# Tool auto-limit untuk file >500MB
# Hanya scan first 1MB

# Split file untuk analyze:
split -b 100M largefile.mp4 part_

# Atau gunakan separate tools:
mediainfo largefile.mp4
```

### Problem: Terminal freeze saat scan
```bash
# Ctrl+C untuk interrupt
Ctrl+C

# Jika tetap hang, kill process:
killall python3

# Run ulang dengan ulimit
ulimit -n 256
python3 hex_editor_tool.py
```

---

## 🔐 Safety First

### Do's ✓
- Always backup sebelum edit
- Test di file copy dulu
- Understand format sebelum modify
- Save reports untuk dokumentasi

### Don'ts ✗
- Jangan edit file system kritis
- Jangan asal write bytes
- Jangan hapus file original
- Jangan pakai root untuk permission

---

## 📞 Support

### Jika ada masalah:
1. Check README.md untuk detail lengkap
2. Test dengan file sample kecil dulu
3. Read error message dengan teliti
4. Check Termux version: `termux -v`
5. Report issue dengan file details

---

## ⚡ Performance Tips

### Untuk File Besar (>100MB)
```bash
# Reduce memory usage
ulimit -v 256000

# Or process in chunks
python3 hex_editor_tool.py
# Gunakan next page [3] bukan load all
```

### Untuk Slow Termux
```bash
# Close background apps
# Run di full screen
# Use landscape orientation untuk better view
# Reduce terminal font size
```

---

## 🎓 Learning Resources

### Understand MP4 Format
- MP4 atom structure
- ftyp = file type
- moov = metadata (required!)
- mdat = actual video data
- free = padding

### Hex Values
- Search dalam hex editor
- Identify patterns
- Learn common magic bytes

### Video Repair
- Check moov box
- Verify atom hierarchy
- Use ffmpeg untuk rebuild

---

## 📝 Contoh Workflow Lengkap

### Kasus: Repair Corrupted MP4

```
Step 1: Jalankan Tool
$ python3 hex_editor_tool.py
(Main menu tampil)

Step 2: Select File
Input: 1
(File browser dibuka)

Step 3: Cari Video Rusak
Cari: Downloads/video.mp4
Input: 1 (select)

Step 4: Scan Struktur
Input: 2
(Scanning...)

Step 5: Lihat Hasil
Jika ada error:
  ⚠️  Missing 'moov' box

Step 6: Try Repair
Input: 3
(ffmpeg process running...)
✓ Repaired file: video.mp4_repaired.mp4

Step 7: Verify Hasil
Input: 2 (scan lagi file baru)
Check output

Step 8: Export Report
Input: 7
✓ Report saved: video.mp4_report.json

Step 9: Done!
Gunakan video.mp4_repaired.mp4
```

---

## 🎯 Next Steps

1. ✓ Setup tool
2. ✓ Browse first file
3. ✓ Try scan feature
4. ✓ Explore hex editor
5. ✓ Practice dengan safe files
6. ✓ Read documentation
7. ✓ Tinggal pake! 🚀

---

**Happy analyzing! - D4nzxml** 👨‍💻

```
Jangan lupa: Backup is life! 💾
```
