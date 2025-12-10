# EXIF Cleaner

A lightweight Windows tool for cleaning EXIF metadata (camera model, GPS, dates, serial numbers, software tags, or *all* EXIF) from JPG and PNG images.  
Built with **Python + Tkinter** and powered by **ExifTool**.

## 🚀 Features

- Remove specific EXIF fields:
  - Serial numbers  
  - Camera model & lens model  
  - GPS metadata  
  - Date/time tags  
  - Software tag  
- Or wipe **all EXIF data** at once  
- Optional: create backups of original files  
- Folder-based batch processing  
- Live progress bar & log output  
- Cancel the cleaning process anytime  
- Remembers your ExifTool path via a config file  
- Simple, fast, no-nonsense UI

## 📦 Requirements

- **Windows**
- **Python 3.x**
- **ExifTool** (exiftool.exe)

Download ExifTool from:  
https://exiftool.org/

## 🛠 Setup

1. Install Python 3 (if not installed).  
2. Ensure Tkinter is available (included by default on Windows).  
3. Download or clone this project.  
4. Install ExifTool and note its path.

## ▶️ How to Use

1. Run the script:
   ```bash
   python exif_cleaner.py
   ```
2. Click **"Select exiftool.exe"** and choose your ExifTool file.  
3. Choose which EXIF tags you want to remove.  
4. Click **"Select Folder"** and pick a folder containing images.  
5. Watch the progress bar and log as files are processed.  
6. Cancel anytime.

## 📁 File Support

- `.jpg`
- `.jpeg`
- `.png`

## ⚙️ Configuration

The app stores your ExifTool path in:

```
%APPDATA%/ExifCleaner/config.json
```

This allows automatic loading of your ExifTool location on startup.

## 🧱 Building a Standalone EXE (Optional)

Use **PyInstaller**:

```bash
pip install pyinstaller
pyinstaller --noconsole --onefile exif_cleaner.py
```

The EXE will appear inside the `dist/` folder.

## 📝 Notes

- EXIF removal is permanent unless **"Create Backup of Originals"** is enabled.  
- PNG files contain fewer metadata fields, so some removals may have no effect.  
- Processing happens in a background thread to keep the interface responsive.

## 🐛 Troubleshooting

**App says ExifTool is not selected**  
→ Make sure you selected the actual `exiftool.exe`.

**No images detected**  
→ Confirm the folder contains .jpg/.jpeg/.png files.

**UI freezes**  
→ Rare, but ensure you're running Python 3.9+.

---

Happy cleaning! ✨
