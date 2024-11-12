from PIL.Image import Image
import tkinter as tk

class ImageData:
    def __init__(self, original: Image, thumbnail: Image, edited_copy: Image, name: str) -> None:
        self.name = name                    # image name
        self.original = original            # raw image
        self.thumbnail = thumbnail          # thumbnail
        self.edited_copy = edited_copy      # image
        self.font_size = tk.StringVar()     # font size
        self.font_name = tk.StringVar()     # font name
        self.color = tk.StringVar()         # text color (RGBA) format
        self.txt_position = (0, 0)          # text position
        self.angle = int                    # angle
        self.is_grid = bool                 # grid option selected
        self.spacing = (0, 0)               # grid option spacing
