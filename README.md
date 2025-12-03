# Bingo Photo Viewer

A lightweight, fullscreen photo viewer application built with Python and Tkinter for displaying images from a local directory in random order.

## Features

- 🎲 **Random Shuffle**: Photos are randomized each time the application launches
- ⌨️ **Keyboard Navigation**: Simple controls using arrow keys or Enter
- 🖼️ **Fullscreen Display**: Immersive viewing experience with black background
- 📊 **Progress Tracking**: Shows current photo number (e.g., "1/56")
- 🔄 **Recursive Scanning**: Automatically finds images in subdirectories
- 🚀 **Optimized Performance**: Uses efficient image resizing to prevent memory issues
- 📺 **Multi-Monitor Support**: Can be displayed on external screens/TVs

## Supported Image Formats

- JPEG (`.jpg`, `.jpeg`)
- PNG (`.png`)
- GIF (`.gif`)
- BMP (`.bmp`)
- TIFF (`.tiff`)
- WebP (`.webp`)

**Note**: HEIC files are not supported in this version.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/justineillusion/bingo_viewer.git
   cd bingo_viewer
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Place your photos** in the `~/Documents/bingo` directory (or any subdirectory within it)

2. **Run the application**:
   ```bash
   python3 bingo_viewer.py
   ```

3. **Navigate through photos**:
   - **Next photo**: Press `Right Arrow` or `Enter`
   - **Previous photo**: Press `Left Arrow`
   - **Exit**: Press `Escape`

## Configuration

You can modify the image directory by editing the `IMAGE_DIR` variable in `bingo_viewer.py`:

```python
IMAGE_DIR = os.path.expanduser("~/Documents/bingo")
```

## Using with External Displays

When using with screen mirroring or external displays (like a TV):

1. Connect your external display
2. Run the application
3. The window will open in fullscreen on your primary display
4. You can drag it to your external display if needed

## Troubleshooting

### Application freezes or crashes
- The application has been optimized to handle large images efficiently
- If you experience issues, ensure your images are not corrupted
- Check that you have sufficient RAM available

### No images found
- Verify that images are placed in `~/Documents/bingo`
- Ensure image files have supported extensions
- Check file permissions

### Application quits unexpectedly with screen mirroring
- This may be related to display connection stability
- Check your TV/monitor connection
- Ensure your system's display settings are stable

## Requirements

- Python 3.6+
- Pillow (PIL)
- Tkinter (usually included with Python)

## License

This project is open source and available for personal use.

## Contributing

Feel free to submit issues or pull requests if you have suggestions for improvements!
