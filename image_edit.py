import os
from PIL import Image, ImageDraw, ImageFont, ImageTk
import tkinter as tk
from tkinter import ttk, Frame

COLORS = ["black", "white", "red", "green", "blue", "yellow", "purple", "orange"]
FONT_SIZES = ["10", "12", "14", "16", "18", "20", "24", "28", "32", "36"]


class ImageEdit:
    '''this class controls the actual image editing functionality'''
    def __init__(self, index: int, controller, callback):
        # Stores the original image and initializes editing parameters
        self.image_index = index
        self.image = None
        self.controller = controller
        self.font_size = tk.StringVar(value=FONT_SIZES[5])
        self.font_name = tk.StringVar()
        self.fonts_names = [] # List to store font names and extensions as tuples
        self.text = tk.StringVar(value="Text goes here")
        self.color = tk.StringVar(value="red")
        self.mouse_pos = (200, 200)
        self.angle = 0
        self.is_grid = tk.StringVar(value='False')  # grid option selection
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
        self.edit_window.geometry("800x500")
        self.edit_window.title('Text Information')
        self.edit_window.resizable(width=True, height=True)
        # screen container
        self.container = tk.Frame(self.edit_window)
        self.container.pack(fill="both", expand=True)

        # Configure columns for layout: lower weight for columns 0-1, higher for 2-7
        self.container.grid_columnconfigure(0, weight=1, uniform='group1')
        self.container.grid_columnconfigure(1, weight=1, uniform='group1')
        self.container.grid_columnconfigure((2, 3, 4, 5, 6, 7), weight=3,
                                         uniform='group1')  # Higher weight for image columns
        # Ensure rows can expand
        for row in range(2):
            self.container.rowconfigure(row, weight=1)

        # Frame for edit options
        self.edit_frame = ttk.Frame(self.container, borderwidth=1, relief='solid')
        self.edit_frame.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=3, pady=3)
        # Configure columns to center-align widgets
        self.edit_frame.grid_columnconfigure(0, weight=1)  # Empty space on the left
        self.edit_frame.grid_columnconfigure((1,2), weight=0)  # Widgets column
        self.edit_frame.grid_columnconfigure(3, weight=1)  # Empty space on the right

        for row in range(11):
            self.edit_frame.grid_rowconfigure(row, weight=0)

        # Font size menu
        self.font_size_label = ttk.Label(self.edit_frame, text='Font Size')
        self.font_size_label.grid(row=0, column=1, columnspan=2, sticky="nsew", padx=3, pady=3)
        self.font_size_dropdown = ttk.Combobox(self.edit_frame, textvariable=self.font_size, values=FONT_SIZES)
        self.font_size_dropdown.grid(row=1, column=1, columnspan=2, sticky="nsew", padx=3, pady=3)

        # fonts names menu
        self.font_name_label = ttk.Label(self.edit_frame, text='Font Name')
        self.font_name_label.grid(row=2, column=1, columnspan=2, sticky="nsew", padx=3, pady=3)
        self.font_dropdown = ttk.Combobox(self.edit_frame, textvariable=self.font_name, values=self.fonts_names, state="readonly")
        self.font_dropdown.grid(row=3, column=1, columnspan=2, sticky="nsew", padx=3, pady=3)

        # text menu
        self.text_label = ttk.Label(self.edit_frame, text='Enter Text')
        self.text_label.grid(row=4, column=1, columnspan=2, sticky="nsew", padx=3, pady=3)
        self.enter_text_entry = tk.Entry(self.edit_frame, textvariable=self.text)
        self.enter_text_entry.grid(row=5, column=1, columnspan=2, sticky="nsew", padx=3, pady=3)

        # color menu
        self.color_label = ttk.Label(self.edit_frame, text='Pick a color')
        self.color_label.grid(row=6, column=1, columnspan=2, sticky="nsew", padx=3, pady=3)
        self.color_dropdown = ttk.Combobox(self.edit_frame, textvariable=self.color, values=COLORS, state="readonly")
        self.color_dropdown.grid(row=7, column=1, columnspan=2, sticky="nsew", padx=3, pady=3)

        # Angle options
        self.angle_scale = tk.Scale(
            self.edit_frame,
            from_=0,  # Minimum value
            to=360,  # Maximum value
            orient="horizontal",  # Horizontal scale
            label="Rotation Angle",  # Label for the scale
            length=80,  # Width of the scale in pixels
            tickinterval=90,  # Interval for ticks (optional)
            resolution=5,  # Step size (optional)
            command=self.image_angle  # Callback function for updates
        )
        self.angle_scale.grid(row=8, column=1, columnspan=2, sticky="nsew", padx=3, pady=3)

        # Set the default value to 0
        self.angle_scale.set(0)

        # create the grid option checkbox
        self.check_grid = ttk.Checkbutton(self.edit_frame, text='Apply Grid',
                                variable=self.is_grid, command=self.update_preview,
                                onvalue='True', offvalue='False')
        self.check_grid.grid(row=9, column=1, columnspan=2, sticky="nsew", padx=3, pady=3)

        # mouse / text position on image
        self.position_label = tk.Label(self.edit_frame, text=f"Current text position. XY={self.mouse_pos}")
        self.position_label.grid(row=10, column=1, columnspan=2, sticky="nsew", padx=3, pady=3)

        # frame for edit buttons
        self.button_frame = ttk.Frame(self.container, borderwidth=1, relief='solid')
        self.button_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=3, pady=3)
        # Configure columns to center-align widgets
        self.button_frame.grid_columnconfigure(0, weight=1)  # Empty space on the left
        self.button_frame.grid_columnconfigure((1,2), weight=0)  # Widgets column
        self.button_frame.grid_columnconfigure(3, weight=1)  # Empty space on the right

        for row in range(2):
            self.button_frame.grid_rowconfigure(row, weight=1)

        # "Apply Text" button
        self.apply_button = tk.Button(self.button_frame, text="Keep Text", command=self.keep_text)
        self.apply_button.grid(row=0, column=1, columnspan=2, sticky="nsew", padx=3, pady=3)

        # Cancel button
        self.cancel_button = tk.Button(self.button_frame, text="Cancel", command=self.cancel)
        self.cancel_button.grid(row=1, column=1, columnspan=2, sticky="nsew", padx=3, pady=3)

        # Create a Canvas for the image that spans columns 2-7
        self.image_canvas_frame = Frame(self.container, borderwidth=1, relief='solid')
        self.image_canvas_frame.grid(row=0, column=2, rowspan=6, columnspan=6, sticky="nsew", padx=3, pady=3)
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


    def image_angle(self, value):
        self.angle = int(value)
        self.update_preview()

    def update_preview (self, event=None):
        # recover latest version of the edited image from the selected_img dictionary
        self.initialize_image()
        self.image = self.controller.resize_image(self.image, self.image_canvas)

        # Load the selected font for editing
        font_path = os.path.join("fonts", self.font_name.get())
        font_size = int(self.font_size.get())
        try:
            font = ImageFont.truetype(font_path, font_size)
        except IOError:
            font = ImageFont.load_default()

        if self.is_grid.get() == 'True':
            # calculate text size
            text_width, text_height = self.find_text_size(font)
            step_x = self.spacing[0] + text_width
            step_y = self.spacing[1] + text_height
            # adjusts image edges
            end_x = self.image_canvas.winfo_width() - (self.image_canvas.winfo_width() - self.image.width) // 2
            end_y = self.image_canvas.winfo_height() - (self.image_canvas.winfo_height() - self.image.height) // 2
            # loop through image positions and generate images
            for y in range(self.spacing[1], end_y, step_y):
                for x in range(self.spacing[0], end_x, step_x):
                    # call function to generate text image overlay
                    self.generate_image(font, x, y)

        else:
            # adjust coordinate to account for different image ratios
            image_x, image_y = self.convert_coordinates(self.mouse_pos[0], self.mouse_pos[1])
            # call function to generate text image overlay
            self.generate_image(font, image_x, image_y)

        # creates tk image
        self.image_tk = ImageTk.PhotoImage(self.image)
        # Update the canvas image and object dictionary
        x = self.image_canvas.winfo_width() // 2
        y = self.image_canvas.winfo_height() // 2
        self.image_canvas.create_image(x, y, anchor='center', image=self.image_tk)


    def find_text_size(self, font):
        text = self.text.get()
        # Initialize a temporary image and apply the text
        image = Image.new("RGBA", (600, 600), (255, 255, 255, 0))
        draw = ImageDraw.Draw(image)
        # Get the bounding box of the text
        bbox = draw.textbbox((0, 0), text, font=font)
        # Calculate the width and height of the text
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        return int(text_width), int(text_height)


    def convert_coordinates(self, pos_x, pos_y):
        '''transform the mouse coordinates if necessary'''
        # adjust mouse coordinates to account for different image ratios
        gap_x = (self.image_canvas.winfo_width() - self.image.width) // 2
        gap_y = (self.image_canvas.winfo_height() - self.image.height) // 2

        if pos_x < gap_x:
            image_x = gap_x
        elif pos_x > self.image_canvas.winfo_width() - gap_x:
            image_x = self.image_canvas.winfo_width() - gap_x
        else:
            image_x = pos_x - gap_x

        if pos_y < gap_y:
            image_y = gap_y
        elif pos_y > self.image_canvas.winfo_height() - gap_y:
            image_y = self.image_canvas.winfo_height() - gap_y
        else:
            image_y = pos_y - gap_y

        return (image_x, image_y)

    def generate_image(self, font, image_x, image_y):
        '''adds the text layer over, rotates and display image'''
        # Create a separate transparent image for the text
        text_layer = Image.new("RGBA", self.image.size, (255, 255, 255, 0))  # Transparent layer
        draw = ImageDraw.Draw(text_layer)

        # Draw the text at the current position
        draw.text(xy=(image_x, image_y), text=self.text.get(), font=font, fill=self.color.get())

        # Rotate the text layer
        rotated_text_layer = text_layer.rotate(self.angle, center=(image_x, image_y))
        box = (0, 0, self.image.width, self.image.height)
        rotated_text_layer.crop(box)

        # Paste rotated text layer onto the original image
        self.image = Image.alpha_composite(self.image.convert("RGBA"), rotated_text_layer)


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


