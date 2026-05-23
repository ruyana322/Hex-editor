# Hex Reference Guide

## Common Hex Values

### Control Characters
```
00 = NULL (null byte)
0A = LF (line feed, \n)
0D = CR (carriage return, \r)
09 = TAB (\t)
20 = SPACE
FF = 255 (maximum byte value)
```

### File Format Magic Bytes

#### Image Formats
```
FF D8 FF E0 = JPEG (JFIF)
FF D8 FF E1 = JPEG (Exif)
89 50 4E 47 = PNG
47 49 46 38 = GIF
42 4D       = BMP
49 49 2A 00 = TIFF (little-endian)
4D 4D 00 2A = TIFF (big-endian)
```

#### Video Formats
```
00 00 00 18 66 74 79 70 = MP4 ftyp box (isom)
00 00 00 20 66 74 79 70 = MP4 ftyp box (isom variant)
66 74 79 70             = MP4/MOV (just "ftyp")
6D 6F 6F 76             = MP4/MOV moov box
6D 64 61 74             = MP4/MOV mdat box
52 49 46 46             = AVI/WAV (RIFF)
1A 45 DF A3             = MKV/WebM (EBML)
```

#### Audio Formats
```
FF FB = MP3 (MPEG sync)
FF FA = MP3 (MPEG sync, MPEG 2)
49 44 33 = MP3 with ID3 tag
66 4C 61 43 = FLAC
4F 67 67 53 = OGG
```

#### Document Formats
```
25 50 44 46 = PDF (%PDF)
50 4B 03 04 = ZIP/XLSX/DOCX
42 5A 68    = BZIP2
1F 8B 08    = GZIP
```

#### Archive Formats
```
50 4B 03 04 = ZIP
50 4B 05 06 = ZIP (end)
50 4B 07 08 = ZIP (span)
37 7A BC AF = 7Z
52 61 72 21 = RAR
```

## ASCII to Hex Conversion

### Common Words
```
"ftyp" = 66 74 79 70
"moov" = 6D 6F 6F 76
"mdat" = 6D 64 61 74
"free" = 66 72 65 65
"wide" = 77 69 64 65
"uuid" = 75 75 69 64
"mvhd" = 6D 76 68 64
"trak" = 74 72 61 6B
"mdia" = 6D 64 69 61
"minf" = 6D 69 6E 66
"stbl" = 73 74 62 6C
```

### Numbers & Symbols
```
"0" = 30
"1" = 31
"9" = 39
"A" = 41
"Z" = 5A
"a" = 61
"z" = 7A
"@" = 40
"#" = 23
"$" = 24
"%" = 25
"&" = 26
"*" = 2A
```

## Byte Value Meanings

### Range: 00-1F (Control)
```
00-08 = Control chars
09 = TAB
0A = Line feed
0B = Vertical tab
0C = Form feed
0D = Carriage return
0E-1F = Other controls
```

### Range: 20-7E (Printable ASCII)
```
20-2F = Space, !, ", #... /
30-39 = 0-9 (numbers)
3A-40 = :, ;, <, =, >, ?, @
41-5A = A-Z (uppercase)
5B-60 = [, \, ], ^, `, `
61-7A = a-z (lowercase)
7B-7E = {, |, }, ~
```

### Range: 7F-FF (Extended/High)
```
7F = DEL
80-FF = Extended ASCII / UTF-8 high bytes
```

## Common Patterns to Search

### MP4/Video Related
```
MP4 header:       00 00 00 18 66 74 79 70
JPEG start:       FF D8 FF
PNG start:        89 50 4E 47
Video box:        74 72 61 6B  (trak)
Audio box:        61 75 64 69  (audi)
```

### Data Patterns
```
Null padding:     00 00 00 00 (repeated)
Repeated 0xFF:    FF FF FF FF (repeated)
Text marker:      00 00 00 20
Size declaration: XX XX XX XX (4-byte big-endian size)
```

## Endianness Reference

### Big-Endian (Network byte order)
```
Value 0x12345678 stored as:
12 34 56 78
```

### Little-Endian (Intel x86)
```
Value 0x12345678 stored as:
78 56 34 12
```

**MP4 uses BIG-ENDIAN!**

## Size Calculations

### Box Size from Hex
```
If size bytes = 00 00 10 00
Convert: 0x00001000 = 4096 bytes

If size bytes = 00 00 00 20
Convert: 0x00000020 = 32 bytes
```

### Common Sizes
```
32 bytes  = 00 00 00 20
64 bytes  = 00 00 00 40
128 bytes = 00 00 00 80
256 bytes = 00 00 01 00
512 bytes = 00 00 02 00
1 KB      = 00 00 04 00
1 MB      = 00 10 00 00
```

## Checksum/Hash Patterns

### SHA256 (32 bytes)
```
Example: AB CD EF 01 23 45 67 89 AB CD EF 01 23 45 67 89
         AB CD EF 01 23 45 67 89 AB CD EF 01 23 45 67 89
```

### MD5 (16 bytes)
```
Example: 5D 41 40 2A BC 4B 2A 76 B9 71 9D 91 10 17 C5 92
```

## Tools for Conversion

Online Hex Converters:
- ASCII → Hex
- Hex → ASCII
- Decimal → Hex
- Binary → Hex

In this tool:
- Search hex: "FF D8 FF"
- Search ASCII: "hello"
- Auto-detect jenis search

## Quick Reference Card

```
NULL byte:     00
Space:         20
@:             40
A-Z:           41-5A (41=A, 5A=Z)
a-z:           61-7A (61=a, 7A=z)
DEL:           7F
Max byte:      FF

Hex Notation:
  0x = hex prefix
  FF = 255 in decimal
  00 = 0 in decimal
  AB = 171 in decimal
```

## Common Search Patterns

### Find All JPEG Images
Search: FF D8 FF
Count all results

### Find All MP4 Atoms
Search: ftyp → moov → mdat
Map locations

### Find Text Strings
Search: hello, copyright, etc.
Use ASCII search

### Find Null Blocks
Search: 00 00 00 00
Repeat searching

## Practical Examples

### Example 1: Find JPEG in Binary File
```
Search: FF D8 FF E0
Result: Found at 0x001A2B4
Extract from that offset until FF D9
```

### Example 2: Find All "hello"
```
Search: hello (ASCII)
Results: All offsets where "hello" appears
```

### Example 3: Identify File Type
```
Check first 8 bytes:
FF D8 FF → JPEG
89 50 4E → PNG
00 00 00 → MP4 (probably)
```

---

*Reference compiled for Hex Editor Tool by D4nzxml*
