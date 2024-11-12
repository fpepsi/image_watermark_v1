import os
from PIL import ImageDraw, ImageFont, ImageTk
import tkinter as tk
from tkinter import ttk, Widget, Frame

COLORS = ["black", "white", "red", "green", "blue", "yellow", "purple", "orange"]
FONT_SIZES = ["10", "12", "14", "16", "18", "20", "24", "28", "32", "36"]


class ImageEdit:
    '''this class controls the actual image editing functionality'''
    def __init__(self, index: int, controller, callback):
        # Stores the original image and initializes editing parameters
        self.image_index = index
        self.image = tk.Image
        self.controller = controller
        self.font_size = tk.StringVar(value=FONT_SIZES[2])
        self.font_name = tk.StringVar()
        self.fonts_names = [] # List to store font names and extensions as tuples
        self.text = tk.StringVar(value="Text goes here")
        self.color = tk.StringVar(value="red")
        self.mouse_pos = (200, 200)
        self.mouse_position = tuple
        self.angle = int
        self.is_grid = bool  # grid option selected
        self.spacing = (50, 50)
        self.callback = callback
        # import font files from 'fonts' directory
        self.initialize_fonts()
        self.initialize_image()


    def initialize_fonts(self):
            # Check if the fonts directory exists
            if os.path.isdir('fonts'):
                # Loop through each file in the directory
                for file_name in os.listdir('fonts'):
                    # Check if the file has a font extension
                    if file_name.endswith((".ttf", ".otf", ".ttc")):
                        self.fonts_names.append(file_name)
                self.font_name.set(self.fonts_names[0])


    def initialize_image(self):
        dict_key = self.controller.key_list[self.image_index]
        self.image = self.controller.selected_img[dict_key].edited_copy

    def window_layout(self):
        '''requests editing information from user'''
        self.edit_window = tk.Toplevel()
        self.edit_window.geometry("800x600")
        self.edit_window.title('Text Information')
        self.edit_window.resizable(width=True, height=True)
        # screen container
        self.container = tk.Frame(self.edit_window)
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        # Configure columns for layout: lower weight for columns 0-1, higher for 2-7
        self.container.columnconfigure(0, weight=1, uniform='group1')
        self.container.columnconfigure(1, weight=1, uniform='group1')
        self.container.columnconfigure((2, 3, 4, 5, 6, 7), weight=3,
                                         uniform='group1')  # Higher weight for image columns
        # Ensure rows can expand
        for row in range(8):
            self.container.rowconfigure(row, weight=1)

        # Font size menu
        self.font_size_dropdown = ttk.Combobox(self.container, textvariable=self.font_size, values=FONT_SIZES)
        self.font_size_dropdown.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

        # fonts names menu
        self.font_dropdown = ttk.Combobox(self.container, textvariable=self.font_name, values=self.fonts_names, state="readonly")
        self.font_dropdown.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

        # text menu
        self.enter_text_entry = tk.Entry(self.container, textvariable=self.text)
        self.enter_text_entry.grid(row=2, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

        # color menu
        self.color_dropdown = ttk.Combobox(self.container, textvariable=self.color, values=COLORS, state="readonly")
        self.color_dropdown.grid(row=3, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

        # mouse / text position on image
        self.position_label = tk.Label(self.container, text=f"Click on the image to select position. XY={self.mouse_pos}")
        self.position_label.grid(row=4, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

        # "Apply Text" button
        self.apply_button = tk.Button(self.container, text="Keep Text", command=self.keep_text)
        self.apply_button.grid(row=5, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

        # Cancel button
        self.cancel_button = tk.Button(self.container, text="Cancel", command=self.cancel)
        self.cancel_button.grid(row=7, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

        # Create a Canvas for the image that spans columns 2-7
        self.image_canvas_frame = Frame(self.container)
        self.image_canvas_frame.grid(row=0, column=2, rowspan=6, columnspan=6, sticky="nsew", padx=10, pady=10)
        self.image_canvas = tk.Canvas(self.image_canvas_frame, background='#133E87')
        self.image_canvas.pack(expand=True, fill="both")

        # Update preview on option change
        self.font_size_dropdown.bind("<<ComboboxSelected>>", lambda e: self.update_preview())
        self.color_dropdown.bind("<<ComboboxSelected>>", lambda e: self.update_preview())
        self.font_dropdown.bind("<<ComboboxSelected>>", lambda e: self.update_preview())
        self.enter_text_entry.bind("<KeyRelease>", lambda e: self.update_preview())

        # Bind resize event to dynamically adjust image size on the canvas
        self.image_canvas.bind("<Configure>", self.update_preview)

        # Function to handle mouse click on image and update position
        self.image_canvas.bind("<Button-1>", lambda event: self.set_position(event))

        # Keep the popup window open
        self.edit_window.grab_set()
        self.edit_window.wait_window(self.edit_window)


    def update_preview (self, event=None):
        self.initialize_image()
        self.image = self.controller.resize_image(self.image, self.image_canvas)
        draw = ImageDraw.Draw(self.image)
        # Load the selected font
        font_path = os.path.join("fonts", self.font_name.get())
        font_size = int(self.font_size.get())
        try:
            font = ImageFont.truetype(font_path, font_size)
        except IOError:
            font = ImageFont.load_default()

        # adjust mouse coordinates to account for different image ratios
        gap_x = (self.image_canvas.winfo_width() - self.image.width) // 2
        gap_y = (self.image_canvas.winfo_height() - self.image.height) // 2

        if self.mouse_pos[0] < gap_x:
            image_x = gap_x
        elif self.mouse_pos[0] > self.image_canvas.winfo_width() - gap_x:
            image_x = self.image_canvas.winfo_width() - gap_x
        else:
            image_x = self.mouse_pos[0] - gap_x

        if self.mouse_pos[1] < gap_y:
            image_y = gap_y
        elif self.mouse_pos[1] > self.image_canvas.winfo_height() - gap_y:
            image_y = self.image_canvas.winfo_height() - gap_y
        else:
            image_y = self.mouse_pos[1] - gap_y

        # Draw the text at the current position
        draw.text(xy=(image_x, image_y), text=self.text.get(), font=font, fill=self.color.get())
        self.image_tk = ImageTk.PhotoImage(self.image)

        # Update the canvas image and object dictionary
        x = self.image_canvas.winfo_width() // 2
        y = self.image_canvas.winfo_height() // 2
        self.image_canvas.create_image(x, y, anchor='center', image=self.image_tk)


    def set_position(self, event):
        """Set the position for text based on a mouse click."""
        # Adjust position relative to the displayed image
        self.mouse_pos = (event.x, event.y)
        self.position_label.config(text=f"Click on the image to select position. \n mouse={self.mouse_pos}")
        self.update_preview()  # Update preview to show text at new position


    # Apply text changes to original image and close pop-up window
    def keep_text(self):
        # stores the edited PIL image in the respective object
        # Close the popup window and resume code on edit_screen
        dict_key = self.controller.key_list[self.image_index]
        self.controller.selected_img[dict_key].edited_copy = self.image
        self.edit_window.destroy()
        self.callback()


    def cancel(self):
        """
        does not apply any editing to the original image
        """
        self.edit_window.destroy()


