import os
import sys
import tkinter as tk
from tkinter import Widget
import main_screen as ms
import edit_screen as es
from PIL import Image
from tkinter.messagebox import askyesno
# TODO 1:  Add a module to insert a logo
# TODO 2: Add a module to fill an image with copyright text

# creates 'images', 'images_wm' folders if non-existent
if not os.path.isdir('images'):
  os.mkdir('images')

if not os.path.isdir('images_wm'):
  os.mkdir('images_wm')


class WatermarkApp(tk.Tk):
    def __init__(self):
        super().__init__()
        # creates app framework - base container for other screens and image dictionary
        self.frames = {}                        # set of app frames
        self.title("Image Watermark Editor")    # app screen title
        self.resizable(width=True, height=True) # allows user to adjust screen size
        self.selected_img = {}                  # stores all image objects
        self.key_list = []                      # list of image dictionary keys
        self.platform = 'darwin' if sys.platform == 'darwin' else 'windows' if sys.platform.startswith(
            'win') else 'linux'                 # Determine the platform and set it as an attribute

        # dimensions app screen to be 3/4 of user screen
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        window_width = int(screen_width * 3) // 4
        window_height = int(screen_height * 3) // 4

        # Calculate the x and y coordinates for the window
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        # Set the window's position and inside Frame
        self.geometry("{}x{}+{}+{}".format(window_width, window_height, x, y))

        # the container is where app frames will be stacked
        # relevant screen display via tk.raise()
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Create screen instances and add them to the screens dictionary
        # main_screen is used to select and preview images to be edited
        # edit_screen focus on each selected image for a better editing experience
        main_screen = ms.MainScreen(parent=container, controller=self)
        main_screen.grid(row=0, column=0, sticky="nsew")
        edit_screen = es.EditScreen(parent=container, controller=self)
        edit_screen.grid(row=0, column=0, sticky="nsew")

        self.frames["main_screen"] = main_screen
        self.frames["edit_screen"] = edit_screen

        self.show_frame("main_screen")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()
        if page_name == 'edit_screen':
            frame.update_canvas()
            frame.button_status()


# TODO: adjust for new image object class
    def close_app(self):
        '''This function closes all open images and the root window'''
        answer = askyesno(title="Exit", message="Do you want to exit?")
        if answer:
            self.destroy()
        else:
            pass


    @staticmethod
    def resize_image(image: Image.Image, widget: Widget, event=None) -> Image.Image:
        # adjust image size to fit canvas with same image ratio
        current_img = image
        cur_img_ratio = current_img.size[0] / current_img.size[1]
        widget_width = widget.winfo_width()
        widget_height = widget.winfo_height()
        canvas_ratio = widget_width / widget_height

        # calculate image sizes to maintain image ratio on canvas
        if canvas_ratio > cur_img_ratio:  # canvas is wider than the image
            height = widget_height
            width = int(height * cur_img_ratio)
        else:  # canvas is narrower than the image
            width = widget_width
            height = int(width / cur_img_ratio)

        current_img = current_img.resize((width, height), Image.Resampling.LANCZOS)
        return current_img



if __name__ == '__main__':
    app = WatermarkApp()
    app.mainloop()

# TODO 2: Create screen which will display selected image and action button
# next button replaces the screen and uploads the first image of the image_pool()
# the back button switches the window back to its previous state
# TODO 3: Create text and logo toolboxes
# TODO 4: Create last window with file format options