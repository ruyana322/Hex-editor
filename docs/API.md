# Hex Editor Tool - API Documentation

## Overview

This document describes the internal API of hex_editor_tool.py for developers who want to extend or integrate the tool.

## Module Structure

```
hex_editor_tool.py
├── Colors (class)
├── FileManager (class)
├── VideoAnalyzer (class)
├── HexEditor (class)
├── VideoRepair (class)
├── ReportGenerator (class)
└── main() (function)
```

---

## Classes Reference

### Colors

Utility class for terminal colors.

**Attributes:**
```python
HEADER      # Purple
OKBLUE      # Blue
OKCYAN      # Cyan
OKGREEN     # Green
WARNING     # Yellow
FAIL        # Red
ENDC        # Reset
BOLD        # Bold text
UNDERLINE   # Underlined text
GRAY        # Gray
LIGHT_GRAY  # Light gray
```

**Usage:**
```python
print(f"{Colors.OKGREEN}Success!{Colors.ENDC}")
```

---

### FileManager

Handle file and directory operations.

**Methods:**

#### `__init__(start_path: str = None)`
Initialize with optional starting path.

```python
fm = FileManager("/home/user")
```

#### `list_directory(path: str = None) -> List[dict]`
List files and folders in directory.

```python
items = fm.list_directory()
# Returns: [{'name': '📁 folder/', 'path': '/path', 'is_dir': True, 'size': '-'}, ...]
```

#### `format_size(bytes_size: int) -> str`
Format bytes to human-readable size.

```python
size_str = FileManager.format_size(1048576)
# Returns: "1.00 MB"
```

#### `browse_files() -> Optional[str]`
Interactive file browser.

```python
selected_file = fm.browse_files()
# Returns: "/path/to/selected/file" or None
```

---

### VideoAnalyzer

Analyze video file structure.

**Attributes:**
```python
file_path: str      # Path to file
file_size: int      # File size in bytes
COMMON_VIDEO_SIGNATURES: dict  # Format detection signatures
```

**Methods:**

#### `__init__(file_path: str)`
Initialize analyzer.

```python
analyzer = VideoAnalyzer("/path/to/video.mp4")
```

#### `scan_structure() -> dict`
Scan complete file structure.

```python
result = analyzer.scan_structure()
# Returns: {
#   'file_info': {...},
#   'headers': [...],
#   'errors': [...]
# }
```

#### `detect_format(data: bytes) -> str`
Detect file format from magic bytes.

```python
format_name = analyzer.detect_format(file_data)
# Returns: "MP4 (ISOM)" or "Unknown Format"
```

#### `scan_mp4_boxes(file_obj, data: bytes) -> list`
Parse MP4 box structure.

```python
boxes = analyzer.scan_mp4_boxes(file, data)
# Returns: [{'offset': 0, 'type': 'ftyp', 'size': 32, ...}, ...]
```

#### `check_common_issues(data: bytes) -> list`
Check for corruption patterns.

```python
issues = analyzer.check_common_issues(data)
# Returns: ["⚠️ Missing 'moov' box", ...]
```

#### `calculate_hash(algorithm: str) -> str`
Calculate file hash.

```python
md5_hash = analyzer.calculate_hash('md5')
sha256_hash = analyzer.calculate_hash('sha256')
# Returns: "abc123def456..."
```

---

### HexEditor

Binary file editing.

**Attributes:**
```python
file_path: str      # Path to file
offset: int         # Current view offset
data: bytearray     # File data in memory
modified: bool      # Changes made flag
```

**Methods:**

#### `__init__(file_path: str)`
Initialize editor and load file.

```python
editor = HexEditor("/path/to/file")
```

#### `load_file()`
Load file into memory.

```python
editor.load_file()
```

#### `view_hex(start_offset: int = 0, num_lines: int = 20)`
Display hex view.

```python
next_offset = editor.view_hex(0, 20)
# Displays 20 lines of hex, returns next offset
```

#### `search_hex(search_term: str) -> list`
Search for hex or ASCII.

```python
results = editor.search_hex("FF D8 FF")
results = editor.search_hex("hello")
# Returns: [offset1, offset2, ...] or []
```

#### `write_bytes(offset: int, data: str) -> bool`
Write bytes at offset.

```python
success = editor.write_bytes(0x100, "FF D8 FF E0")
# Returns: True if success, False if error
```

#### `save_file(backup: bool = True) -> bool`
Save changes to file.

```python
success = editor.save_file()
# Returns: True if success, creates backup
```

---

### VideoRepair

Video repair utilities.

**Methods:**

#### `repair_mp4_moov(file_path: str) -> bool`
Attempt to repair MP4 file.

```python
success = VideoRepair.repair_mp4_moov("/path/to/video.mp4")
# Returns: True if repaired, False otherwise
# Creates: video.mp4_repaired.mp4
```

---

### ReportGenerator

Generate analysis reports.

**Methods:**

#### `generate_report(analysis_result: dict, file_path: str) -> str`
Generate JSON report.

```python
report_path = ReportGenerator.generate_report(analysis_data, "/path/to/file")
# Returns: "/path/to/file_report.json"
# Creates: JSON file with analysis results
```

---

## Usage Examples

### Example 1: Basic File Analysis

```python
from hex_editor_tool import FileManager, VideoAnalyzer

# Select file
fm = FileManager()
file_path = fm.browse_files()

# Analyze
analyzer = VideoAnalyzer(file_path)
result = analyzer.scan_structure()

# Print result
print(f"Format: {result['file_info']['detected_format']}")
print(f"Size: {result['file_info']['size_human']}")
for error in result['errors']:
    print(f"Issue: {error}")
```

### Example 2: Hex Search & Edit

```python
from hex_editor_tool import HexEditor

editor = HexEditor("/path/to/file")

# Search
results = editor.search_hex("FF D8 FF")
print(f"Found at: {[hex(r) for r in results]}")

# Edit
editor.write_bytes(0x100, "00 00 00 00")

# Save
editor.save_file()
```

### Example 3: Auto Repair

```python
from hex_editor_tool import VideoAnalyzer, VideoRepair

analyzer = VideoAnalyzer("/path/to/video.mp4")
result = analyzer.scan_structure()

if any("moov" in str(e) for e in result['errors']):
    success = VideoRepair.repair_mp4_moov("/path/to/video.mp4")
    if success:
        # Verify repair
        analyzer2 = VideoAnalyzer("/path/to/video.mp4_repaired.mp4")
        result2 = analyzer2.scan_structure()
```

### Example 4: Generate Report

```python
from hex_editor_tool import VideoAnalyzer, ReportGenerator

analyzer = VideoAnalyzer("/path/to/file")
result = analyzer.scan_structure()

report_path = ReportGenerator.generate_report(result, "/path/to/file")
print(f"Report saved to: {report_path}")
```

---

## Data Structures

### File Info Dictionary

```python
{
    'path': str,                    # Full file path
    'filename': str,                # Filename only
    'size': int,                    # Size in bytes
    'size_human': str,              # Formatted size
    'modified': str,                # ISO timestamp
    'md5': str,                     # MD5 hash
    'sha256': str,                  # SHA256 hash
    'detected_format': str          # Format name
}
```

### Box Dictionary

```python
{
    'offset': int,                  # Byte offset
    'type': str,                    # 4-char box type
    'size': int,                    # Size in bytes
    'size_human': str               # Formatted size
}
```

### Search Result

```python
List[int]  # List of offsets where pattern found
# Example: [0, 1024, 2048]
```

---

## Constants

### Supported Video Formats

```python
COMMON_VIDEO_SIGNATURES = {
    b'\x00\x00\x00\x18ftypmp42': 'MP4 (MP42)',
    b'\x00\x00\x00\x20ftypisom': 'MP4 (ISOM)',
    b'\x00\x00\x00\x14ftypqt': 'MOV (QuickTime)',
    b'ftyp': 'MP4/MOV Format',
    b'\x1a\x45\xdf\xa3': 'WebM/MKV',
    # ... more formats
}
```

---

## Error Handling

All methods use try-except internally.

**Common Exceptions:**

```python
FileNotFoundError       # File doesn't exist
PermissionError         # No read/write access
ValueError              # Invalid input
struct.error            # Binary parsing error
```

**Returns:**

Methods return appropriate types:
- Booleans for success/failure
- None for no results
- Lists/dicts for data
- Strings for messages

---

## Configuration

### Environment Variables

```bash
export HEX_NO_BACKUP=1          # Disable backups
export HEX_TEMP=/custom/path    # Custom temp dir
```

### Programmatic Configuration

```python
# (To be implemented in v1.1.0)
import hex_editor_tool
hex_editor_tool.CONFIG['backup_on_save'] = False
```

---

## Performance Notes

- File loading: O(n) where n = file size
- Search: O(n) linear search
- Hash calculation: O(n) streaming
- Structure scanning: O(n) limited to first 1MB

For large files (>500MB):
- Only first 1MB scanned
- Search limited to memory-loaded portion
- Use streaming for analysis

---

## Future API Extensions

v1.1.0+ planned:

```python
# Plugin system
class HexEditorPlugin:
    def analyze(self, data: bytes) -> dict
    def repair(self, file_path: str) -> bool

# Configuration system
class Config:
    def load(self, config_file: str)
    def save(self, config_file: str)

# Async operations
async def analyze_async(file_path: str)
async def repair_async(file_path: str)
```

---

## Contributing

To extend this tool:

1. Follow existing code style
2. Add docstrings to new methods
3. Include type hints
4. Write tests
5. Update documentation
6. Submit pull request

---

**API Version**: 1.0.0
**Tool Version**: 1.0.0
**Last Updated**: January 2024
**Author**: D4nzxml
