import os
import time
import sys
from PIL import Image
import psutil

def get_memory_usage():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024  # MB

def create_large_image(filename, size=(8000, 6000)):
    print(f"Creating {filename} with size {size}...")
    img = Image.new('RGBA', size, color='red')
    img.save(filename)
    print(f"Created. File size: {os.path.getsize(filename) / 1024 / 1024:.2f} MB")

def simulate_load_and_resize(filename):
    print(f"Initial Memory: {get_memory_usage():.2f} MB")
    
    start_time = time.time()
    
    # Simulate the app's logic
    print("Opening image...")
    pil_image = Image.open(filename)
    print(f"After Open Memory: {get_memory_usage():.2f} MB")
    
    screen_width = 1920
    screen_height = 1080
    
    img_width, img_height = pil_image.size
    ratio = min(screen_width / img_width, screen_height / img_height)
    new_width = int(img_width * ratio)
    new_height = int(img_height * ratio)
    
    print(f"Resizing to {screen_width}x{screen_height} using thumbnail...")
    # The app uses thumbnail now
    pil_image.thumbnail((screen_width, screen_height), Image.Resampling.LANCZOS)
    
    print(f"After Resize Memory: {get_memory_usage():.2f} MB")
    print(f"Time taken: {time.time() - start_time:.2f}s")
    
    return pil_image

if __name__ == "__main__":
    filename = "test_large.png"
    if not os.path.exists(filename):
        create_large_image(filename)
    
    try:
        simulate_load_and_resize(filename)
    finally:
        if os.path.exists(filename):
            os.remove(filename)
