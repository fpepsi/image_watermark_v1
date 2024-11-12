from tkinter import Frame, Canvas, Button
from PIL import Image, ImageTk
import base_screen as bs
from image_edit import ImageEdit
from file_save import SaveImageDialog


class EditScreen(bs.BaseScreen):
    '''This class manages the selected images' editing options and interactions,
     allowing user to navigate through larger images and chose editing tools'''
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.parent = parent         # main.py container frame
        self.controller = controller # main.py watermarkapp object
        self.image_index = 0         # controls image_list position

        # screen layout setup
        # Configure the columns
        for i in range(6):  # First 6 columns with equal width
            self.columnconfigure(i, weight=2)

        self.columnconfigure(6, weight=1)  # Last column with half the width
        # Configure the rows
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=0)

        # Top button Frame -
        self.top_button_frame = Frame(self, bg='#F3F3E0', pady=10)
        self.top_button_frame.grid(column=1, columnspan=5, row=0, sticky='nsew')

        # Configure columns in top_button_frame for even spacing
        for i in range(5):
            self.top_button_frame.columnconfigure(i, weight=1)

        # top buttons
        self.back_button = Button(self.top_button_frame,
                                  text="Back",
                                  bg='#CBDCEB',
                                  bd=0,
                                  highlightthickness=0,
                                  highlightcolor='#133E87',
                                  command=lambda: controller.show_frame("main_screen"))
        self.back_button.grid(column=0, row=0, pady=5, padx=5, ipadx=5, ipady=5, sticky='nsew')

        # place holder button to support additional app screens
        # self.next_button = Button(self.top_button_frame,
        #                           text="Next",
        #                           bg='#CBDCEB',
        #                           bd=0,
        #                           highlightthickness=0,
        #                           state='disabled',
        #                           highlightcolor='#133E87',
        #                           command=lambda: controller.show_frame("main_screen"))
        # self.next_button.grid(column=2, row=0, pady=5, padx=5, ipadx=5, ipady=5, sticky='nsew')
        # quits the app
        self.quit_button = Button(self.top_button_frame,
                                  text="Quit Program",
                                  bg='#CBDCEB',
                                  bd=0,
                                  highlightthickness=0,
                                  highlightcolor='#133E87',
                                  command=lambda: controller.close_app())
        self.quit_button.grid(column=4, row=0, pady=5, padx=5, ipadx=5, ipady=5, sticky='nsew')

        # editing options
        # left button Frame
        self.left_button_frame = Frame(self, bg='#F3F3E0')
        self.left_button_frame.grid(column=0, row=1, sticky='nsew')

        # Configure column in left_button_frame for even spacing
        self.left_button_frame.columnconfigure(0, weight=1)

        # left frame buttons
        # takes selected image to text editing screen
        self.add_txt_btn = Button(self.left_button_frame,
                                  text="Add Text",
                                  bg='#CBDCEB',
                                  bd=0,
                                  highlightthickness=0,
                                  highlightcolor='#133E87',
                                  justify='center',
                                  command=lambda: self.start_editing(),
                                  )
        self.add_txt_btn.grid(column=0, row=0, pady=30, padx=30, ipadx=5, ipady=5, sticky='nsew')
        # takes selected image to logo editing screen - images can hole logos and text
        self.add_logo = Button(self.left_button_frame,
                                  text="Add Logo",
                                  bg='#CBDCEB',
                                  bd=0,
                                  highlightthickness=0,
                                  state='normal',
                                  highlightcolor='#133E87',
                               justify='center',
                                  )
        self.add_logo.grid(column=0, row=1, pady=30, padx=30, ipadx=5, ipady=5, sticky='nsew')
        # logic to apply the editing style of current image to all images
        # self.apply_all = Button(self.left_button_frame,
        #                         text="Apply to All",
        #                         bg='#CBDCEB',
        #                         bd=0,
        #                         highlightthickness=0,
        #                         highlightcolor='#133E87',
        #                         command=lambda: self.apply_all_text()
        #                         )
        # self.apply_all.grid(column=0, row=2, pady=30, padx=30, ipadx=5, ipady=5, sticky='nsew')
        # restore image's original state
        self.clear_img = Button(self.left_button_frame,
                                  text="Clear Img",
                                  bg='#CBDCEB',
                                  bd=0,
                                  highlightthickness=0,
                                  highlightcolor='#133E87',
                                justify='center',
                                command=lambda: self.revert_changes(),
                                  )
        self.clear_img.grid(column=0, row=3, pady=30, padx=30, ipadx=5, ipady=5, sticky='nsew')
        # opens the file save menu
        self.save = Button(self.left_button_frame,
                                text="Save Image",
                                bg='#CBDCEB',
                                bd=0,
                                highlightthickness=0,
                                highlightcolor='#133E87',
                                command=lambda: self.save_edited()
                                )
        self.save.grid(column=0, row=2, pady=30, padx=30, ipadx=5, ipady=5, sticky='nsew')

        # right Frame - empty
        self.right_frame = Frame(self, bg='#F3F3E0', padx=10)
        self.right_frame.grid(column=6, row=1, sticky='nsew')

        # Bottom button Frame - moves between selected images
        self.bottom_button_frame = Frame(self, bg='#F3F3E0')
        self.bottom_button_frame.grid(column=1, columnspan=5, row=3, sticky='nsew')

        # Configure columns in bottom_button_frame for even spacing
        for i in range(5):
            self.bottom_button_frame.columnconfigure(i, weight=1)

        # bottom buttons
        self.previous_img = Button(self.bottom_button_frame,
                                  text="Previous Image",
                                  bg='#CBDCEB',
                                  bd=0,
                                  highlightthickness=0,
                                  highlightcolor='#133E87',
                                   state='disabled',
                                   command=lambda: self.previous_image()
                                   )
        self.previous_img.grid(column=1, row=0, pady=30, padx=30, ipadx=5, ipady=5, sticky='nsew')

        self.next_img = Button(self.bottom_button_frame,
                                   text="Next Image",
                                   bg='#CBDCEB',
                                   bd=0,
                                   highlightthickness=0,
                                   highlightcolor='#133E87',
                               state='disabled',
                               command=lambda: self.next_image()
                               )
        self.next_img.grid(column=3, row=0, pady=30, padx=30, ipadx=5, ipady=5, sticky='nsew')


        # Central canvas - displays one edited image at a time
        # when canvas is modified, a configure event calls function to resize image for proper fit
        self.canvas_frame = Frame(self)
        self.canvas_frame.grid(column=1, columnspan=5, row=1, sticky='nsew')

        self.canvas = Canvas(self.canvas_frame,
                             background='#133E87',
                             highlightthickness=0,
                             relief='ridge')
        self.canvas.pack(expand=True, fill="both")

        # Bind to Configure event to update canvas
        self.canvas.bind("<Configure>", self.update_canvas)

        self.button_status() # adjust image flow button status to reflect current image selection

    def button_status(self):
        '''adjust image flow button status to reflect current image selection'''
        if len(self.controller.key_list) == 0:
            pass
        else:
            if len(self.controller.key_list) == 1:
                self.next_img.config(state='disabled')
                self.previous_img.config(state='disabled')
            elif self.image_index == 0 and len(self.controller.key_list) > 1:
                self.next_img.config(state='normal')
                self.previous_img.config(state='disabled')
            elif self.image_index == len(self.controller.key_list) - 1:
                self.next_img.config(state='disabled')
                self.previous_img.config(state='normal')
            else:
                self.next_img.config(state='normal')
                self.previous_img.config(state='normal')


    def next_image(self):
        '''moves to next selected image'''
        if self.image_index < len(self.controller.key_list) - 1:
            self.image_index += 1
            self.button_status()
            self.update_canvas()
        else:
            pass

    def previous_image(self):
        '''moves to previous selected image'''
        if self.image_index > 0:
            self.image_index -= 1
            self.button_status()
            self.update_canvas()
        else:
            pass


    def revert_changes(self):
        ''' restores image with original status'''
        dict_key = self.controller.key_list[self.image_index]
        self.controller.selected_img[dict_key].edited_copy = self.controller.selected_img[dict_key].original
        self.update_canvas()


    def update_canvas(self, event=None):
        '''Resizes the image_list image referenced by image_index and refreshes the canvas'''
        if len(self.controller.key_list) > 0:
            image_key = self.controller.key_list[self.image_index]
            # resizes the image for proper fit
            resize_image = self.controller.selected_img[image_key].edited_copy
            # Convert resized PIL image to PhotoImage, place it on canvas center
            self.canvas_img = ImageTk.PhotoImage(self.controller.resize_image(resize_image, self.canvas))
            x = self.canvas.winfo_width() // 2
            y = self.canvas.winfo_height() // 2
            self.canvas.create_image(x, y, anchor='center', image=self.canvas_img)


    def start_editing(self):
        drawing_board = ImageEdit(index=self.image_index, controller=self.controller, callback=self.update_canvas)
        drawing_board.window_layout()


    def save_edited(self):
        '''controls edited image file generation'''
        dict_key = self.controller.key_list[self.image_index]
        filename = self.controller.selected_img[dict_key].name
        save_box = SaveImageDialog(root=self.left_button_frame, filename=filename, initial_dir='images_wm/')
        save_box.open_save_dialog()
        # Wait until the dialog is closed and a file path is set
        self.left_button_frame.wait_window(save_box.dialog)

        # Check if a file path has been selected
        file_path = save_box.file_name.get()
        if file_path:
            try:
                # Save the image with the chosen extension
                self.controller.selected_img[dict_key].edited_copy.save(file_path)
                print(f"Image saved successfully at: {file_path}")
            except Exception as e:
                print(f"Failed to save image: {e}")
