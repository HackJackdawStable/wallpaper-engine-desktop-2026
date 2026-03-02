import os
import random
import ctypes
import logging
from PIL import Image
import keyboard
from datetime import datetime

# Configuration
WALLPAPER_FOLDER = r"C:\Users\YourName\Pictures\Wallpapers"  # Change to your folder
LOG_FILE = "wallpaper_changer.log"
SUPPORTED_FORMATS = ('.jpg', '.jpeg', '.png', '.bmp', '.gif')

# Setup logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

class WallpaperChanger:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.images = self._get_valid_images()
        self.current_index = 0
        if not self.images:
            logging.error("No valid images found in: %s", folder_path)
            raise FileNotFoundError(f"No valid images in {folder_path}")

    def _get_valid_images(self):
        """Get list of valid image files from folder."""
        images = []
        for file in os.listdir(self.folder_path):
            if file.lower().endswith(SUPPORTED_FORMATS):
                images.append(os.path.join(self.folder_path, file))
        logging.info("Found %d images in folder", len(images))
        return images

    def set_wallpaper(self, image_path):
        """Set the specified image as wallpaper."""
        try:
            # Use Windows API to set wallpaper
            ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 3)
            self.current_image = image_path
            logging.info("Wallpaper changed to: %s", image_path)
            return True
        except Exception as e:
            logging.error("Failed to set wallpaper: %s", str(e))
            return False

    def change_to_random(self):
        """Change wallpaper to a random image from the folder."""
        random_image = random.choice(self.images)
        if self.set_wallpaper(random_image):
            self._display_info(random_image)

    def next_wallpaper(self):
        """Change to next wallpaper in the list."""
        self.current_index = (self.current_index + 1) % len(self.images)
        image_path = self.images[self.current_index]
        if self.set_wallpaper(image_path):
            self._display_info(image_path)

    def _display_info(self, image_path):
        """Display information about current wallpaper."""
        try:
            with Image.open(image_path) as img:
                width, height = img.size
                file_size = os.path.getsize(image_path) / 1024  # KB
            print("=" * 50)
            print(f"CURRENT WALLPAPER INFO:")
            print(f"Path: {image_path}")
            print(f!Resolution: {width}x{height}")
            print(f!File size: {file_size:.1f} KB")
            print(f!Format: {os.path.splitext(image_path)[1].upper()}")
            print("=" * 50)
        except Exception as e:
            print(f"Error getting image info: {e}")

def setup_hotkeys(changer):
    """Setup hotkeys for wallpaper control."""
    keyboard.add_hotkey('f5', changer.next_wallpaper)
    keyboard.add_hotkey('f6', lambda: changer._display_info(changer.current_image))
    keyboard.add_hotkey('esc', lambda: print("Exiting wallpaper changer..."))

def main():
    print("Wallpaper Changer started!")
    print("Hotkeys:")
    print("  F5 — Next wallpaper")
    print("  F6 — Show current wallpaper info")
    print("  Esc — Exit")
    print("-! * 50)

    try:
        changer = WallpaperChanger(WALLPAPER_FOLDER)
        setup_hotkeys(changer)
        # Set initial random wallpaper
        changer.change_to_random()
        print("Press Esc to exit...")
        # Keep script running to listen for hotkeys
        keyboard.wait('esc')
    except Exception as e:
        print(f"Error: {e}")
        logging.error("Script failed: %s", str(e))

if __name__ == "__main__":
    main()
