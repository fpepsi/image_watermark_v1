import os
from tkinter import Frame, Canvas, Scrollbar, Button, Label, filedialog
from PIL import Image, ImageTk
import base_screen as bs
import image_object as io
import mouse_scroll

THUMBNAIL_SIZE = (300, 300)


class MainScreen(bs.BaseScreen):
    '''This class manages opening image files and storing them in objects.
    'parent' is the container frame from main.py
    controller is the WatermarkApp object'''
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        self.thumbnail_images = []    # will keep  persistent copy of thumbnails
        # layout setup 3 x 3 grid with large second line
        self.columnconfigure((0,1,2), weight=1, uniform='a')
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=0)

        # Top button Frame controls app screen flow
        self.top_button_frame = Frame(self, bg='#F3F3E0')
        self.top_button_frame.grid(column=0, columnspan=3, row=0, sticky='nsew')

        # Configure columns in top_button_frame for even spacing
        for i in range(3):
            self.top_button_frame.columnconfigure(i, weight=1)

        # Top frame buttons
        # upload_button will open filedialog for image file selection
        self.upload_button = Button(self.top_button_frame,
                                    text="Select Images",
                                    bg='#CBDCEB',
                                    bd=0,
                                    highlightthickness=0,
                                    justify='center', # in case text too long
                                    command=self.select_images)
        self.upload_button.grid(column=0, row=0, pady=5, padx=5, ipadx=5, ipady=5, sticky='nsew')
        # next_button will be activated once images are selected and take us to edit_screen
        self.next_button = Button(self.top_button_frame,
                                  text="Next",
                                  bg='#CBDCEB',
                                  bd=0,
                                  highlightthickness=0,
                                  justify='center',
                                  state='disabled',
                                  command=lambda: controller.show_frame("edit_screen"))
        self.next_button.grid(column=1, row=0, pady=5, padx=5, ipadx=5, ipady=5, sticky='nsew')
        # quit_button will quit the app
        self.quit_button = Button(self.top_button_frame,
                                  text="Quit Program",
                                  bg='#CBDCEB',
                                  bd=0,
                                  highlightthickness=0,
                                  justify='center',
                                  command=lambda: controller.close_app())
        self.quit_button.grid(column=2, row=0, pady=5, padx=5, ipadx=5, ipady=5, sticky='nsew')

        # Canvas with Scrollbar
        # the canvas will display a list of selected images' thumbnails
        self.canvas_frame = Frame(self)
        self.canvas_frame.grid(column=0, columnspan=3, row=1, sticky='nsew')
        self.canvas = Canvas(self.canvas_frame,
                             background='#133E87',
                             highlightthickness=0,
                             relief='ridge')
        self.canvas.pack(side="left", expand=True, fill="both")
        self.scroll_y = Scrollbar(self.canvas_frame,
                                  orient="vertical",
                                  command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scroll_y.set)

        # Initial label on canvas
        # This is guidance on how user should proceed to select different images
        self.canvas.create_text(200, 100, text="Selected Images go Here", fill="white", font=('Helvetica', 16))

        # Adjust canvas scroll region based on image layout
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Bind mouse wheel scrolling to the canvas
        mouse_scroll.bind_mouse_scroll(widget=self.canvas)

        # Instruction label
        self.instruction_label = Label(self, text="Review selected images and press 'Select Images' to reselect if needed.",
                                bg='#F3F3E0', font=('Helvetica', 12))
        self.instruction_label.grid(column=0, columnspan=3, row=2, pady=10)
        self.instruction_label.grid_remove()  # Hide initially


    def select_images(self):
        ''' this function is called to allow selection of images to be edited
        It allows many simultaneous selections from files placed under "/images" folder'''
        files = filedialog.askopenfiles(mode='r',
                                        parent=self.parent,
                                        title='Select Images',
                                        initialdir='/images',
                                        filetypes=(('Image Files', '*.jpeg *.jpg *.png'),
                                                   ('All Files', '*.*')))
        if files:
           # Clear canvas and remove label if present
           self.canvas.delete("all")

           # the loop below creates one object per image and stores them on a dictionary
           # it also creates image thumbnails and aligns them evenly for display on the canvas
           x, y = 10, 10    # Initial position for the thumbnails
           counter = 1      # indexes the selected images
           for file in files:
               key = 'image_' + str(counter)
               counter += 1
               filename = os.path.basename(file.name).split('.')[0]
               original = Image.open(file.name)
               thumbnail = original.copy()
               thumbnail.thumbnail(THUMBNAIL_SIZE, resample=Image.Resampling.NEAREST)
               edited_copy = original.copy()
               self.controller.selected_img[key] = io.ImageData(name=filename,
                                                                original=original,
                                                                thumbnail=thumbnail,
                                                                edited_copy=edited_copy)


               # Add each image to the canvas
               thumbnail_tk = ImageTk.PhotoImage(thumbnail)
               self.thumbnail_images.append(thumbnail_tk)
               self.canvas.create_image(x, y, anchor='nw', image=thumbnail_tk)
               x += THUMBNAIL_SIZE[0] + 10  # Move position for the next thumbnail
               if x > self.canvas.winfo_width() - THUMBNAIL_SIZE[0] - 10:  # Wrap to next row if needed
                   x = 10
                   y += THUMBNAIL_SIZE[1] + 10

           # Show scrollbar only if content exceeds the visible canvas height
           if y > self.canvas.winfo_height() - 10:
               self.scroll_y.pack(side="right", fill="y")
           else:
               self.scroll_y.pack_forget()

           self.instruction_label.grid() # Show the instruction label
           self.next_button.configure(state='normal') # activate "next" button

           # if there are images uploaded, list them based on the selected_img dictionary
           self.controller.key_list = list(self.controller.selected_img.keys())

        else:
           self.next_button.configure(state='disabled')

