import os
import random
import sys
import argparse
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
try:
    # Optimization: Increase max image pixels to avoid DecompressionBombError for large photos
    Image.MAX_IMAGE_PIXELS = None
except AttributeError:
    pass

# Configuration
IMAGE_DIR = os.path.expanduser("~/Documents/bingo")
SUPPORTED_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp')

class BingoViewer:
    def __init__(self, root, image_dir):
        self.root = root
        self.root.title("Bingo Photo Viewer")
        self.root.attributes('-fullscreen', True)
        self.root.configure(background='black')
        
        # Bind keys
        self.root.bind('<Return>', self.next_image)
        self.root.bind('<Right>', self.next_image)
        self.root.bind('<Left>', self.prev_image)
        self.root.bind('<Escape>', self.close)
        
        self.image_paths = self.load_images(image_dir)
        print(f"Found {len(self.image_paths)} images in {image_dir}")
        
        if not self.image_paths:
            messagebox.showerror("Error", f"No images found in {image_dir}")
            self.root.destroy()
            return
            
        random.shuffle(self.image_paths)
        self.current_index = 0
        
        self.canvas = tk.Canvas(root, bg='black', highlightthickness=0)
        self.canvas.pack(expand=True, fill='both')
        
        self.show_image()
        
    def load_images(self, directory):
        images = []
        if not os.path.exists(directory):
            try:
                os.makedirs(directory)
                print(f"Created directory: {directory}")
            except OSError as e:
                print(f"Error creating directory: {e}")
                return []
        
        # Walk recursively
        for root, dirs, files in os.walk(directory):
            for filename in files:
                if filename.lower().endswith(SUPPORTED_EXTENSIONS):
                    images.append(os.path.join(root, filename))
        return images

    def show_image(self):
        if not self.image_paths:
            return
            
        # Update title with progress
        self.root.title(f"Bingo Photo Viewer - {self.current_index + 1}/{len(self.image_paths)}")
            
        image_path = self.image_paths[self.current_index]
        
        try:
            pil_image = Image.open(image_path)
            
            # Resize image to fit screen while maintaining aspect ratio
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            
            # Use thumbnail for faster resizing and memory efficiency
            # It modifies the image in place and preserves aspect ratio
            pil_image.thumbnail((screen_width, screen_height), Image.Resampling.LANCZOS)
            
            self.photo = ImageTk.PhotoImage(pil_image)
            
            self.canvas.delete("all")
            # Center the image
            x_center = screen_width // 2
            y_center = screen_height // 2
            self.canvas.create_image(x_center, y_center, image=self.photo, anchor='center')
            
            # Add number overlay
            # Top-left corner, large white text with black outline for visibility
            text = str(self.current_index + 1)
            
            # Better: Draw black text slightly offset, then white text on top
            self.canvas.create_text(52, 52, text=text, font=("Arial", 48, "bold"), fill="black", anchor='nw')
            self.canvas.create_text(50, 50, text=text, font=("Arial", 48, "bold"), fill="white", anchor='nw')
            
        except Exception as e:
            print(f"Error processing image {image_path}: {e}")
            
    def next_image(self, event=None):
        if self.current_index < len(self.image_paths) - 1:
            self.current_index += 1
            self.show_image()
        else:
            self.root.title(f"Bingo Photo Viewer - End of Slideshow ({len(self.image_paths)}/{len(self.image_paths)})")
            print("End of list reached.")

    def prev_image(self, event=None):
        if self.current_index > 0:
            self.current_index -= 1
            self.show_image()

    def close(self, event=None):
        self.root.destroy()

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description='Bingo Photo Viewer - Display photos in random order',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        '--folder', '-f',
        type=str,
        default='bingo',
        help='Source folder name within ~/Documents/ (default: "bingo")'
    )
    
    args = parser.parse_args()
    
    # Construct image directory from folder argument
    image_dir = os.path.expanduser(f"~/Documents/{args.folder}")
    
    root = tk.Tk()
    app = BingoViewer(root, image_dir)
    root.mainloop()
