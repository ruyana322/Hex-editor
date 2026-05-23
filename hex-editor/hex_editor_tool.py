#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
╔════════════════════════════════════════════════════════════════╗
║           HEX EDITOR - Video Binary Analysis Tool              ║
║                     by D4nzxml                                 ║
╚════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import struct
import json
import hashlib
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Tuple
import shutil

# Colors untuk terminal
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    GRAY = '\033[90m'
    LIGHT_GRAY = '\033[37m'

def clear_screen():
    os.system('clear' if os.name != 'nt' else 'cls')

def print_header():
    header = f"""
{Colors.BOLD}{Colors.OKCYAN}
╔════════════════════════════════════════════════════════════════╗
║           HEX EDITOR - Video Binary Analysis Tool              ║
║                     by D4nzxml                                 ║
╚════════════════════════════════════════════════════════════════╝
{Colors.ENDC}
"""
    print(header)

def print_menu():
    menu = f"""
{Colors.OKBLUE}┌─ MAIN MENU ─────────────────────────────────────────┐{Colors.ENDC}
{Colors.OKGREEN}[1]{Colors.ENDC} 📂 Browse & Select File
{Colors.OKGREEN}[2]{Colors.ENDC} 🔍 Scan Struktur Video
{Colors.OKGREEN}[3]{Colors.ENDC} 🔧 Repair Video
{Colors.OKGREEN}[4]{Colors.ENDC} 📊 Analyzer Metadata
{Colors.OKGREEN}[5]{Colors.ENDC} ⚡ Faststar Optimizer
{Colors.OKGREEN}[6]{Colors.ENDC} ⚠️  Check Corruption
{Colors.OKGREEN}[7]{Colors.ENDC} 📝 Export Report
{Colors.OKGREEN}[8]{Colors.ENDC} ✏️  Edit Write File Biner
{Colors.OKGREEN}[0]{Colors.ENDC} Exit
{Colors.OKBLUE}└──────────────────────────────────────────────────────┘{Colors.ENDC}
"""
    print(menu)

class FileManager:
    def __init__(self, start_path: str = None):
        self.current_path = start_path or str(Path.home())
        self.selected_file = None
        
    def list_directory(self, path: str = None) -> List[dict]:
        if path:
            self.current_path = path
        
        items = []
        try:
            entries = sorted(os.listdir(self.current_path))
            for entry in entries:
                full_path = os.path.join(self.current_path, entry)
                if os.path.isdir(full_path):
                    items.append({
                        'name': f"📁 {entry}/",
                        'path': full_path,
                        'is_dir': True,
                        'size': '-'
                    })
                else:
                    size = os.path.getsize(full_path)
                    size_str = self.format_size(size)
                    items.append({
                        'name': f"📄 {entry}",
                        'path': full_path,
                        'is_dir': False,
                        'size': size_str
                    })
        except PermissionError:
            print(f"{Colors.FAIL}❌ Permission denied!{Colors.ENDC}")
        
        return items
    
    @staticmethod
    def format_size(bytes_size: int) -> str:
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes_size < 1024.0:
                return f"{bytes_size:.2f} {unit}"
            bytes_size /= 1024.0
        return f"{bytes_size:.2f} TB"
    
    def browse_files(self) -> Optional[str]:
        clear_screen()
        print_header()
        
        while True:
            print(f"\n{Colors.BOLD}{Colors.OKCYAN}Current Path:{Colors.ENDC} {self.current_path}\n")
            
            items = self.list_directory()
            
            # Add parent directory option
            if self.current_path != '/':
                print(f"{Colors.WARNING}[..] Go Up{Colors.ENDC}")
                for i, item in enumerate(items, 1):
                    print(f"{Colors.OKGREEN}[{i}]{Colors.ENDC} {item['name']} {Colors.GRAY}({item['size']}){Colors.ENDC}")
            else:
                for i, item in enumerate(items, 1):
                    print(f"{Colors.OKGREEN}[{i}]{Colors.ENDC} {item['name']} {Colors.GRAY}({item['size']}){Colors.ENDC}")
            
            choice = input(f"\n{Colors.OKBLUE}Pilih file/folder (.. untuk naik, 0 back): {Colors.ENDC}").strip()
            
            if choice == '0':
                return None
            elif choice == '..':
                parent = os.path.dirname(self.current_path)
                if parent != self.current_path:
                    self.current_path = parent
            else:
                try:
                    idx = int(choice) - 1
                    if 0 <= idx < len(items):
                        selected = items[idx]
                        if selected['is_dir']:
                            self.current_path = selected['path']
                        else:
                            return selected['path']
                except (ValueError, IndexError):
                    print(f"{Colors.FAIL}Invalid choice!{Colors.ENDC}")

class VideoAnalyzer:
    COMMON_VIDEO_SIGNATURES = {
        b'\x00\x00\x00\x18ftypmp42': 'MP4 (MP42)',
        b'\x00\x00\x00\x20ftypisom': 'MP4 (ISOM)',
        b'\x00\x00\x00\x20ftypiso2': 'MP4 (ISO2)',
        b'\x00\x00\x00\x14ftypqt': 'MOV (QuickTime)',
        b'ftyp': 'MP4/MOV Format',
        b'\xff\xfb': 'MP3',
        b'ID3': 'MP3 with ID3',
        b'RIFF': 'AVI/WAV',
        b'\x1a\x45\xdf\xa3': 'WebM/MKV',
    }
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.file_size = os.path.getsize(file_path)
        
    def scan_structure(self) -> dict:
        """Scan struktur video file"""
        result = {
            'file_info': {},
            'headers': [],
            'errors': []
        }
        
        try:
            result['file_info'] = {
                'path': self.file_path,
                'filename': os.path.basename(self.file_path),
                'size': self.file_size,
                'size_human': FileManager.format_size(self.file_size),
                'modified': datetime.fromtimestamp(os.path.getmtime(self.file_path)).isoformat(),
                'md5': self.calculate_hash('md5'),
                'sha256': self.calculate_hash('sha256')
            }
            
            with open(self.file_path, 'rb') as f:
                # Read first 1MB untuk scan
                data = f.read(min(1024 * 1024, self.file_size))
                
                # Detect format
                detected_format = self.detect_format(data)
                result['file_info']['detected_format'] = detected_format
                
                # Scan boxes/atoms (untuk MP4)
                if 'MP4' in detected_format or 'MOV' in detected_format:
                    result['headers'] = self.scan_mp4_boxes(f, data)
                elif 'WebM' in detected_format or 'MKV' in detected_format:
                    result['headers'] = [{'type': 'EBML', 'description': 'Matroska Format Detected'}]
                
                # Check untuk common issues
                result['errors'] = self.check_common_issues(data)
                
        except Exception as e:
            result['errors'].append(f"Error scanning: {str(e)}")
        
        return result
    
    def detect_format(self, data: bytes) -> str:
        """Detect format dari magic bytes"""
        for signature, format_name in self.COMMON_VIDEO_SIGNATURES.items():
            if data.startswith(signature):
                return format_name
        return "Unknown Format"
    
    def scan_mp4_boxes(self, file_obj, data: bytes) -> list:
        """Scan MP4 box structure"""
        boxes = []
        try:
            offset = 0
            while offset < len(data) - 8:
                size_bytes = data[offset:offset+4]
                if len(size_bytes) < 4:
                    break
                
                size = struct.unpack('>I', size_bytes)[0]
                box_type = data[offset+4:offset+8].decode('ascii', errors='ignore')
                
                if size > 0 and box_type.isprintable():
                    boxes.append({
                        'offset': offset,
                        'type': box_type,
                        'size': size,
                        'size_human': FileManager.format_size(size)
                    })
                    offset += size
                else:
                    offset += 1
        except Exception as e:
            boxes.append({'error': str(e)})
        
        return boxes
    
    def check_common_issues(self, data: bytes) -> list:
        """Check untuk corruption dan issues"""
        issues = []
        
        # Check moov box exists
        if b'moov' not in data:
            issues.append("⚠️  Missing 'moov' box - file may be incomplete")
        
        # Check ftyp at start
        if not data.startswith(b'\x00\x00\x00'):
            issues.append("⚠️  Unusual header - may not be standard MP4")
        
        # Check null bytes (indicator of corruption)
        null_blocks = data.count(b'\x00\x00\x00\x00')
        if null_blocks > 100:
            issues.append(f"⚠️  High number of null blocks detected ({null_blocks})")
        
        return issues
    
    def calculate_hash(self, algorithm: str) -> str:
        """Calculate file hash"""
        try:
            hash_obj = hashlib.new(algorithm)
            with open(self.file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b''):
                    hash_obj.update(chunk)
            return hash_obj.hexdigest()
        except:
            return "N/A"

class HexEditor:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.offset = 0
        self.data = None
        self.modified = False
        self.load_file()
    
    def load_file(self):
        """Load file ke memory"""
        try:
            with open(self.file_path, 'rb') as f:
                self.data = bytearray(f.read())
            self.modified = False
        except Exception as e:
            print(f"{Colors.FAIL}Error loading file: {e}{Colors.ENDC}")
    
    def view_hex(self, start_offset: int = 0, num_lines: int = 20):
        """Display hex view dengan ASCII representation"""
        clear_screen()
        print_header()
        print(f"\n{Colors.BOLD}File:{Colors.ENDC} {self.file_path}")
        print(f"{Colors.BOLD}Size:{Colors.ENDC} {FileManager.format_size(len(self.data))}\n")
        
        print(f"{Colors.OKBLUE}Offset      Hex Data                              ASCII{Colors.ENDC}")
        print(f"{Colors.GRAY}{'─' * 70}{Colors.ENDC}")
        
        for i in range(num_lines):
            offset = start_offset + (i * 16)
            if offset >= len(self.data):
                break
            
            chunk = self.data[offset:offset+16]
            hex_str = ' '.join(f'{b:02x}' for b in chunk)
            ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in chunk)
            
            print(f"{Colors.OKGREEN}{offset:08x}{Colors.ENDC}    {hex_str:<48} {Colors.OKCYAN}{ascii_str}{Colors.ENDC}")
        
        return start_offset + (num_lines * 16)
    
    def search_hex(self, search_term: str) -> list:
        """Search untuk hex atau string"""
        results = []
        try:
            # Try as hex string
            if all(c in '0123456789abcdefABCDEF ' for c in search_term):
                search_bytes = bytes.fromhex(search_term.replace(' ', ''))
            else:
                # Try as ASCII string
                search_bytes = search_term.encode('utf-8')
            
            pos = 0
            while True:
                found = self.data.find(search_bytes, pos)
                if found == -1:
                    break
                results.append(found)
                pos = found + 1
        except Exception as e:
            print(f"{Colors.FAIL}Search error: {e}{Colors.ENDC}")
        
        return results
    
    def write_bytes(self, offset: int, data: str) -> bool:
        """Write bytes pada offset tertentu"""
        try:
            # Parse hex string
            hex_bytes = bytes.fromhex(data.replace(' ', '').replace(',', ''))
            
            if offset + len(hex_bytes) > len(self.data):
                print(f"{Colors.FAIL}Error: Data exceeds file size!{Colors.ENDC}")
                return False
            
            self.data[offset:offset+len(hex_bytes)] = hex_bytes
            self.modified = True
            print(f"{Colors.OKGREEN}✓ Written {len(hex_bytes)} bytes at offset {offset:08x}{Colors.ENDC}")
            return True
        except Exception as e:
            print(f"{Colors.FAIL}Write error: {e}{Colors.ENDC}")
            return False
    
    def save_file(self, backup: bool = True) -> bool:
        """Save changes ke file"""
        try:
            if backup:
                backup_path = self.file_path + '.backup'
                shutil.copy2(self.file_path, backup_path)
                print(f"{Colors.OKGREEN}✓ Backup created: {backup_path}{Colors.ENDC}")
            
            with open(self.file_path, 'wb') as f:
                f.write(self.data)
            
            self.modified = False
            print(f"{Colors.OKGREEN}✓ File saved successfully!{Colors.ENDC}")
            return True
        except Exception as e:
            print(f"{Colors.FAIL}Save error: {e}{Colors.ENDC}")
            return False

class ReportGenerator:
    @staticmethod
    def generate_report(analysis_result: dict, file_path: str) -> str:
        """Generate report dalam format JSON dan text"""
        report = {
            'generated_at': datetime.now().isoformat(),
            'tool_version': '1.0.0',
            'author': 'D4nzxml',
            'analysis': analysis_result
        }
        
        report_json = json.dumps(report, indent=2)
        report_path = file_path + '_report.json'
        
        try:
            with open(report_path, 'w') as f:
                f.write(report_json)
            return report_path
        except Exception as e:
            print(f"{Colors.FAIL}Error generating report: {e}{Colors.ENDC}")
            return None

class VideoRepair:
    """Simple video repair utilities"""
    @staticmethod
    def repair_mp4_moov(file_path: str) -> bool:
        """Attempt to fix MP4 dengan missing moov box"""
        print(f"{Colors.WARNING}🔧 Attempting MP4 repair...{Colors.ENDC}")
        
        # Check jika ffmpeg tersedia
        try:
            result = subprocess.run(
                ['which', 'ffmpeg'],
                capture_output=True,
                timeout=5
            )
            if result.returncode == 0:
                print(f"{Colors.OKBLUE}Using ffmpeg untuk repair...{Colors.ENDC}")
                output_path = file_path + '_repaired.mp4'
                cmd = [
                    'ffmpeg', '-i', file_path,
                    '-c', 'copy', '-y', output_path
                ]
                subprocess.run(cmd, capture_output=True, timeout=30)
                print(f"{Colors.OKGREEN}✓ Repaired file: {output_path}{Colors.ENDC}")
                return True
        except:
            pass
        
        print(f"{Colors.WARNING}⚠️  ffmpeg not available. Manual repair recommended.{Colors.ENDC}")
        return False

def main():
    clear_screen()
    print_header()
    
    file_manager = FileManager()
    selected_file = None
    analyzer = None
    
    while True:
        print_menu()
        
        if selected_file:
            print(f"\n{Colors.OKGREEN}📁 Current File:{Colors.ENDC} {os.path.basename(selected_file)}")
        
        choice = input(f"{Colors.OKBLUE}Enter choice: {Colors.ENDC}").strip()
        
        if choice == '0':
            print(f"\n{Colors.OKGREEN}Thanks for using Hex Editor! Bye bro 👋{Colors.ENDC}\n")
            break
        
        elif choice == '1':
            selected_file = file_manager.browse_files()
            if selected_file:
                print(f"\n{Colors.OKGREEN}✓ File selected: {selected_file}{Colors.ENDC}")
                input("Press Enter to continue...")
        
        elif choice == '2' and selected_file:
            analyzer = VideoAnalyzer(selected_file)
            result = analyzer.scan_structure()
            
            clear_screen()
            print_header()
            print(f"\n{Colors.BOLD}{Colors.OKCYAN}═══ SCAN HASIL ═══{Colors.ENDC}\n")
            print(f"{Colors.OKBLUE}File Info:{Colors.ENDC}")
            for key, value in result['file_info'].items():
                print(f"  {key}: {value}")
            
            if result['headers']:
                print(f"\n{Colors.OKBLUE}Boxes Found:{Colors.ENDC}")
                for box in result['headers'][:20]:  # Limit output
                    if 'type' in box:
                        print(f"  {box['type']:<4} @ {box.get('offset', 'N/A'):>8} ({box.get('size_human', 'N/A')})")
            
            if result['errors']:
                print(f"\n{Colors.WARNING}Issues Detected:{Colors.ENDC}")
                for error in result['errors']:
                    print(f"  {error}")
            
            input("\nPress Enter to continue...")
        
        elif choice == '3' and selected_file:
            VideoRepair.repair_mp4_moov(selected_file)
            input("Press Enter to continue...")
        
        elif choice == '4' and selected_file:
            analyzer = VideoAnalyzer(selected_file)
            result = analyzer.scan_structure()
            
            clear_screen()
            print_header()
            print(f"\n{Colors.BOLD}{Colors.OKCYAN}═══ METADATA ANALYSIS ═══{Colors.ENDC}\n")
            print(json.dumps(result['file_info'], indent=2))
            
            input("\nPress Enter to continue...")
        
        elif choice == '5' and selected_file:
            print(f"\n{Colors.OKBLUE}Coming soon...{Colors.ENDC}")
            input("Press Enter to continue...")
        
        elif choice == '6' and selected_file:
            analyzer = VideoAnalyzer(selected_file)
            result = analyzer.scan_structure()
            
            clear_screen()
            print_header()
            print(f"\n{Colors.BOLD}{Colors.OKCYAN}═══ CORRUPTION CHECK ═══{Colors.ENDC}\n")
            
            if result['errors']:
                print(f"{Colors.FAIL}Issues Found:{Colors.ENDC}")
                for error in result['errors']:
                    print(f"  ❌ {error}")
            else:
                print(f"{Colors.OKGREEN}✓ No issues detected!{Colors.ENDC}")
            
            input("\nPress Enter to continue...")
        
        elif choice == '7' and selected_file:
            analyzer = VideoAnalyzer(selected_file)
            result = analyzer.scan_structure()
            report_path = ReportGenerator.generate_report(result, selected_file)
            
            clear_screen()
            print_header()
            if report_path:
                print(f"\n{Colors.OKGREEN}✓ Report generated:{Colors.ENDC}")
                print(f"  {report_path}\n")
            
            input("Press Enter to continue...")
        
        elif choice == '8' and selected_file:
            hex_editor = HexEditor(selected_file)
            
            while True:
                clear_screen()
                print_header()
                offset = hex_editor.view_hex(hex_editor.offset, 20)
                
                print(f"\n{Colors.OKBLUE}┌─ HEX EDITOR MENU ───────────────────┐{Colors.ENDC}")
                print(f"{Colors.OKGREEN}[1]{Colors.ENDC} Search Hex/String")
                print(f"{Colors.OKGREEN}[2]{Colors.ENDC} Write Bytes")
                print(f"{Colors.OKGREEN}[3]{Colors.ENDC} Next Page")
                print(f"{Colors.OKGREEN}[4]{Colors.ENDC} Save Changes")
                print(f"{Colors.OKGREEN}[0]{Colors.ENDC} Back to Main Menu")
                print(f"{Colors.OKBLUE}└─────────────────────────────────────┘{Colors.ENDC}")
                
                editor_choice = input(f"{Colors.OKBLUE}Choice: {Colors.ENDC}").strip()
                
                if editor_choice == '0':
                    break
                elif editor_choice == '1':
                    search_term = input(f"{Colors.OKBLUE}Search (hex or string): {Colors.ENDC}")
                    results = hex_editor.search_hex(search_term)
                    
                    print(f"\n{Colors.OKGREEN}Found at offsets:{Colors.ENDC}")
                    for i, offset_found in enumerate(results[:10]):
                        print(f"  {i+1}. 0x{offset_found:08x}")
                    
                    input("Press Enter...")
                
                elif editor_choice == '2':
                    offset_str = input(f"{Colors.OKBLUE}Offset (hex): {Colors.ENDC}")
                    data_str = input(f"{Colors.OKBLUE}Data (hex): {Colors.ENDC}")
                    
                    try:
                        offset = int(offset_str, 16)
                        hex_editor.write_bytes(offset, data_str)
                    except ValueError:
                        print(f"{Colors.FAIL}Invalid offset format!{Colors.ENDC}")
                    
                    input("Press Enter...")
                
                elif editor_choice == '3':
                    hex_editor.offset += 320
                    if hex_editor.offset >= len(hex_editor.data):
                        hex_editor.offset = max(0, len(hex_editor.data) - 320)
                
                elif editor_choice == '4':
                    hex_editor.save_file()
                    input("Press Enter...")
        
        elif choice in ['2','3','4','5','6','7','8'] and not selected_file:
            print(f"\n{Colors.FAIL}❌ Please select a file first!{Colors.ENDC}")
            input("Press Enter to continue...")
        
        else:
            print(f"\n{Colors.FAIL}Invalid choice!{Colors.ENDC}")
            input("Press Enter to continue...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.WARNING}Program terminated by user{Colors.ENDC}\n")
        sys.exit(0)
