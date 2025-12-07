import os
import random
from PIL import Image, ImageDraw, ImageFont
import sys
import argparse

# Configuration
IMAGE_DIR = os.path.expanduser("~/Documents/bingo")
SUPPORTED_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp')

# Bingo card settings
GRID_SIZE = 5  # 5x5 grid
NUM_CARDS = 10  # Generate 10 cards
CELL_SIZE = 200  # Size of each cell in pixels
BORDER_WIDTH = 4  # Border between cells
CARD_PADDING = 40  # Padding around the card
TITLE_HEIGHT = 80  # Height for title area
CHECKBOX_SIZE = 30  # Size of checkbox

# Colors
BACKGROUND_COLOR_PINK = (255, 192, 203)  # Pink background (default)
PASTEL_COLORS = [
    (255, 192, 203),  # Pink (original)
    (210, 210, 235),  # Light purple/lavender (from reference image 1)
    (220, 240, 220),  # Light mint green (from reference image 2)
    (210, 230, 240),  # Light blue (from reference image 3)
]
BORDER_COLOR = (0, 0, 0)  # Black borders
TITLE_COLOR = (80, 80, 80)  # Dark gray title
CHECKBOX_COLOR = (255, 255, 255)  # White checkbox background
CHECKBOX_BORDER = (0, 0, 0)  # Black checkbox border

def load_images(directory):
    """Load all images from the directory and subdirectories."""
    images = []
    if not os.path.exists(directory):
        print(f"Error: Directory {directory} does not exist")
        return []
    
    # Walk recursively
    for root, dirs, files in os.walk(directory):
        # Skip the output directory
        if 'bingo_cards' in root:
            continue
        for filename in files:
            if filename.lower().endswith(SUPPORTED_EXTENSIONS):
                images.append(os.path.join(root, filename))
    
    return images

def create_thumbnail(image_path, size):
    """Create a thumbnail of the image."""
    try:
        img = Image.open(image_path)
        # Convert to RGB if necessary (for transparency)
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        
        # Resize to fill the cell (crop to square)
        img.thumbnail((size * 2, size * 2), Image.Resampling.LANCZOS)
        
        # Crop to square
        width, height = img.size
        if width > height:
            left = (width - height) // 2
            img = img.crop((left, 0, left + height, height))
        elif height > width:
            top = (height - width) // 2
            img = img.crop((0, top, width, top + width))
        
        # Final resize to exact cell size
        img = img.resize((size, size), Image.Resampling.LANCZOS)
        return img
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        # Return a placeholder image
        placeholder = Image.new('RGB', (size, size), (200, 200, 200))
        return placeholder

def create_bingo_card(images, card_number, title="J&J's BINGO", background_color=None):
    """Create a single bingo card with random images."""
    # Use default pink if no color specified
    if background_color is None:
        background_color = BACKGROUND_COLOR_PINK
    
    # Calculate card dimensions
    card_width = (CELL_SIZE * GRID_SIZE) + (BORDER_WIDTH * (GRID_SIZE + 1)) + (CARD_PADDING * 2)
    card_height = TITLE_HEIGHT + (CELL_SIZE * GRID_SIZE) + (BORDER_WIDTH * (GRID_SIZE + 1)) + (CARD_PADDING * 2)
    
    # Create the card
    card = Image.new('RGB', (card_width, card_height), background_color)
    draw = ImageDraw.Draw(card)
    
    # Try to load a nice font, fallback to default
    try:
        title_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 48)
    except:
        try:
            title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 48)
        except:
            title_font = ImageFont.load_default()
    
    # Draw title
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (card_width - title_width) // 2
    title_y = (TITLE_HEIGHT - (title_bbox[3] - title_bbox[1])) // 2
    draw.text((title_x, title_y), title, fill=TITLE_COLOR, font=title_font)
    
    # Select random images for this card
    if len(images) < GRID_SIZE * GRID_SIZE:
        print(f"Warning: Not enough images ({len(images)}) for a full {GRID_SIZE}x{GRID_SIZE} card")
        selected_images = random.choices(images, k=GRID_SIZE * GRID_SIZE)
    else:
        selected_images = random.sample(images, GRID_SIZE * GRID_SIZE)
    
    # Draw the grid
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            # Calculate position
            x = CARD_PADDING + (col * (CELL_SIZE + BORDER_WIDTH)) + BORDER_WIDTH
            y = TITLE_HEIGHT + CARD_PADDING + (row * (CELL_SIZE + BORDER_WIDTH)) + BORDER_WIDTH
            
            # Draw border (cell background)
            draw.rectangle(
                [x - BORDER_WIDTH, y - BORDER_WIDTH, 
                 x + CELL_SIZE + BORDER_WIDTH, y + CELL_SIZE + BORDER_WIDTH],
                fill=BORDER_COLOR
            )
            
            # Get and paste the image
            image_index = row * GRID_SIZE + col
            thumbnail = create_thumbnail(selected_images[image_index], CELL_SIZE)
            card.paste(thumbnail, (x, y))
            
            # Draw checkbox below the image
            checkbox_x = x + (CELL_SIZE - CHECKBOX_SIZE) // 2
            checkbox_y = y + CELL_SIZE - CHECKBOX_SIZE - 5
            
            # Draw white checkbox with black border
            draw.rectangle(
                [checkbox_x, checkbox_y, checkbox_x + CHECKBOX_SIZE, checkbox_y + CHECKBOX_SIZE],
                fill=CHECKBOX_COLOR,
                outline=CHECKBOX_BORDER,
                width=2
            )
    
    return card

def sanitize_folder_name(title):
    """Convert title to a valid folder name."""
    # Remove or replace characters that aren't safe for folder names
    # Keep alphanumeric, spaces, hyphens, and underscores
    import re
    # Replace special characters with underscores or remove them
    sanitized = re.sub(r'[^\w\s-]', '', title)
    # Replace spaces with underscores
    sanitized = re.sub(r'\s+', '_', sanitized)
    # Remove leading/trailing underscores
    sanitized = sanitized.strip('_')
    # If empty after sanitization, use a default
    if not sanitized:
        sanitized = "bingo_cards"
    return sanitized

def main():
    """Main function to generate bingo cards."""
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description='Generate random bingo cards from images',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate 10 cards with default title "J&J's BINGO"
  python generate_bingo_cards.py
  
  # Generate cards with custom title
  python generate_bingo_cards.py --title "R&L"
  
  # Generate 20 cards with custom title
  python generate_bingo_cards.py --title "Sarah & Mike" --count 20
        """
    )
    parser.add_argument(
        '--title', '-t',
        type=str,
        default="J&J's BINGO",
        help='Title to display on the bingo cards (default: "J&J\'s BINGO")'
    )
    parser.add_argument(
        '--count', '-c',
        type=int,
        default=NUM_CARDS,
        help=f'Number of bingo cards to generate (default: {NUM_CARDS})'
    )
    parser.add_argument(
        '--multicolour', '-m',
        action='store_true',
        help='Use random pastel colors for each card (default: pink for all cards)'
    )
    
    args = parser.parse_args()
    
    print(f"Loading images from {IMAGE_DIR}...")
    images = load_images(IMAGE_DIR)
    
    if not images:
        print("Error: No images found!")
        return
    
    print(f"Found {len(images)} images")
    
    if len(images) < GRID_SIZE * GRID_SIZE:
        print(f"Warning: You need at least {GRID_SIZE * GRID_SIZE} images for a full bingo card.")
        print("Some images will be repeated.")
    
    # Create output directory based on title
    folder_name = sanitize_folder_name(args.title)
    output_dir = os.path.join(IMAGE_DIR, "bingo_cards", folder_name)
    os.makedirs(output_dir, exist_ok=True)
    print(f"Creating {args.count} bingo cards with title '{args.title}' in {output_dir}...")
    
    # Generate cards
    for i in range(args.count):
        print(f"Generating card {i + 1}/{args.count}...")
        
        # Select background color
        if args.multicolour:
            bg_color = random.choice(PASTEL_COLORS)
        else:
            bg_color = BACKGROUND_COLOR_PINK
        
        card = create_bingo_card(images, i + 1, title=args.title, background_color=bg_color)
        
        # Save the card
        output_path = os.path.join(output_dir, f"bingo_card_{i + 1:02d}.png")
        card.save(output_path, "PNG", quality=95)
        print(f"Saved: {output_path}")
    
    print(f"\n✅ Successfully generated {args.count} bingo cards!")
    print(f"📁 Cards saved in: {output_dir}")

if __name__ == "__main__":
    main()
