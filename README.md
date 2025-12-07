# Bingo Photo Viewer

A lightweight, fullscreen photo viewer application built with Python and Tkinter for displaying images from a local directory in random order.

## Features

### Photo Viewer
- 🎲 **Random Shuffle**: Photos are randomized each time the application launches
- ⌨️ **Keyboard Navigation**: Simple controls using arrow keys or Enter
- 🖼️ **Fullscreen Display**: Immersive viewing experience with black background
- 📊 **Progress Tracking**: Shows current photo number (e.g., "1/56")
- 🔄 **Recursive Scanning**: Automatically finds images in subdirectories
- 🚀 **Optimized Performance**: Uses efficient image resizing to prevent memory issues
- 📺 **Multi-Monitor Support**: Can be displayed on external screens/TVs

### Bingo Card Generator
- 🎨 **Custom Bingo Cards**: Generate 5x5 photo bingo cards from your images
- 🎯 **Customizable Titles**: Add personalized titles to each card set
- 🌈 **Multicolour Mode**: Choose between classic pink or random pastel colors
- 📁 **Organized Output**: Cards are saved in title-based subfolders
- ✅ **Interactive Checkboxes**: Each photo has a checkbox for marking during gameplay

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

### Generating Bingo Cards

The bingo card generator creates printable 5x5 photo bingo cards from your image collection.

1. **Basic usage** (generates 10 pink cards with default title):
   ```bash
   python3 generate_bingo_cards.py
   ```

2. **Custom title**:
   ```bash
   python3 generate_bingo_cards.py --title "R&L"
   ```

3. **Multicolour cards** (random pastel backgrounds):
   ```bash
   python3 generate_bingo_cards.py --title "Sarah & Mike" --multicolour
   ```

4. **Custom number of cards**:
   ```bash
   python3 generate_bingo_cards.py --title "J&J's BINGO" --count 20
   ```

5. **All options combined**:
   ```bash
   python3 generate_bingo_cards.py -t "Wedding Bingo" -c 15 -m
   ```

#### Command-Line Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--title` | `-t` | Title displayed on the cards | `"J&J's BINGO"` |
| `--count` | `-c` | Number of cards to generate | `10` |
| `--multicolour` | `-m` | Use random pastel colors | `False` (pink) |
| `--help` | `-h` | Show help message | - |

#### Output

Cards are saved in `~/Documents/bingo/bingo_cards/<sanitized_title>/`:
- Example: `"R&L"` → `~/Documents/bingo/bingo_cards/RL/`
- Example: `"J&J's BINGO"` → `~/Documents/bingo/bingo_cards/JJs_BINGO/`

Each card is saved as `bingo_card_01.png`, `bingo_card_02.png`, etc.

#### Color Options

**Default (Pink)**: All cards have a classic pink background
```bash
python3 generate_bingo_cards.py --title "My Bingo"
```

**Multicolour**: Cards randomly use one of four pastel colors:
- 🩷 Pink
- 💜 Light purple/lavender
- 💚 Light mint green
- 💙 Light blue

```bash
python3 generate_bingo_cards.py --title "My Bingo" --multicolour
```

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

### Photo Viewer

#### Application freezes or crashes
- The application has been optimized to handle large images efficiently
- If you experience issues, ensure your images are not corrupted
- Check that you have sufficient RAM available

#### No images found
- Verify that images are placed in `~/Documents/bingo`
- Ensure image files have supported extensions
- Check file permissions

#### Application quits unexpectedly with screen mirroring
- This may be related to display connection stability
- Check your TV/monitor connection
- Ensure your system's display settings are stable

### Bingo Card Generator

#### Not enough images warning
- You need at least 25 images for a full 5x5 bingo card
- If you have fewer images, some will be repeated on the cards
- Add more images to `~/Documents/bingo` for better variety

#### Cards look different than expected
- Ensure you're using the `--multicolour` flag if you want varied colors
- Check that your images are in supported formats
- Large images are automatically resized to fit the card cells

#### Output folder not found
- The script automatically creates the output directory
- Check that you have write permissions to `~/Documents/bingo`
- Verify the path exists and is accessible

## Requirements

- Python 3.6+
- Pillow (PIL)
- Tkinter (usually included with Python)

## License

This project is open source and available for personal use.

## Contributing

Feel free to submit issues or pull requests if you have suggestions for improvements!
