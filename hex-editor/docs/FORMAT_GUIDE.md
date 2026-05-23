# MP4 Format Guide

## Structure Overview

MP4 files organized dalam "atoms" (juga disebut "boxes")

```
MP4 File Structure:
├── ftyp (File Type Box) - Identify MP4 format
├── free (Free Space) - Padding
├── mdat (Media Data Box) - Actual video/audio data
└── moov (Movie Box) - Metadata (REQUIRED!)
    ├── mvhd - Movie header
    ├── trak - Track 1 (video)
    │   ├── tkhd
    │   ├── edts
    │   └── mdia
    └── trak - Track 2 (audio)
        ├── tkhd
        ├── edts
        └── mdia
```

## Critical Boxes

### ftyp (File Type Box)
- **Location**: Start of file (usually 32 bytes)
- **Magic**: `00 00 00 20 66 74 79 70`
- **Purpose**: Identify file as MP4
- **Missing = CRITICAL ERROR**

### moov (Movie Box)
- **Location**: End of file (optimal) or middle
- **Contains**: Metadata, codec info, duration
- **Purpose**: Essential untuk playback
- **Missing = File unplayable!**

### mdat (Media Data Box)
- **Location**: Usually after moov
- **Contains**: Actual video/audio frames
- **Size**: Usually largest box

## Box Structure

Each box:
```
4 bytes: Box size (big-endian)
4 bytes: Box type (4 ASCII chars)
N bytes: Box data
```

Example (ftyp box):
```
00 00 00 20 = Size 32 bytes
66 74 79 70 = "ftyp"
69 73 6f 6d = "isom" (brand)
... rest of box data
```

## Common Issues

### Missing moov Box
- **Symptom**: File unplayable, no duration
- **Cause**: Incomplete download or corruption
- **Fix**: Try rebuild dengan ffmpeg

### Out-of-order Atoms
- **Symptom**: Streaming problems
- **Cause**: Bad file creation
- **Fix**: Reorder atoms (mdat first, moov last optimal)

### Corrupted mdat
- **Symptom**: Playback glitches, bad frames
- **Cause**: Data corruption
- **Fix**: Partial recovery possible, not full

### Invalid Sizes
- **Symptom**: Parser errors
- **Cause**: Wrong box size declaration
- **Fix**: Recalculate sizes

## Repair Strategy

1. **Check ftyp** → If missing, file is lost
2. **Check moov** → If missing, try rebuild
3. **Verify atom chain** → Check integrity
4. **Rebuild if needed** → Use ffmpeg
5. **Verify result** → Re-scan after repair

## Hex Patterns to Know

```
ftyp box start:      00 00 00 20 66 74 79 70
moov box start:      00 00 XX XX 6D 6F 6F 76
mdat box start:      00 00 XX XX 6D 64 61 74
MP4 typical header:  00 00 00 18 66 74 79 70 69 73 6F 6D
```

## Tools for Analysis

- **Hex Editor** (this tool): View/edit bytes
- **mediainfo**: Full format analysis
- **ffmpeg**: Repair/convert
- **mp4box**: Detailed atom inspection

## References

- ISO/IEC 14496-12 (MP4 specification)
- Quicktime format (similar to MP4)
- ISOM brand details
