from tkinter import Tk, Toplevel, Label, Button, Listbox, Scrollbar, filedialog, END, StringVar, Entry
from PIL import Image

class SaveImageDialog:
    def __init__(self, root, filename, initial_dir):
        self.root = root
        self.extension = StringVar(value=".png")  # Default extension
        self.file_name = StringVar(value=filename)
        self.file_dir = initial_dir

    def open_save_dialog(self):
        # Create a Toplevel window for selecting the file extension
        self.dialog = Toplevel(self.root)
        self.dialog.title("Save As")
        self.dialog.geometry("300x500")

        Label(self.dialog, text="Select file format:").pack(pady=5)

        # Scrollbar and Listbox for displaying supported file extensions
        scrollbar = Scrollbar(self.dialog)
        scrollbar.pack(side="right", fill="y")

        self.extension_listbox = Listbox(self.dialog, selectmode="single", yscrollcommand=scrollbar.set)
        self.extension_listbox.pack(expand=True, fill="both", padx=10)
        scrollbar.config(command=self.extension_listbox.yview)

        # Populate Listbox with supported file extensions from PIL
        supported_formats = Image.registered_extensions()  # Get all registered extensions
        for ext in supported_formats.keys():
            self.extension_listbox.insert(END, ext)

        # Bind selection event to update the chosen extension
        self.extension_listbox.bind("<<ListboxSelect>>", self.on_select_extension)

        # Entry box for the file name
        Label(self.dialog, text="Enter file name:").pack(pady=5)
        self.file_entry = Entry(self.dialog, textvariable=self.file_name, width=30)
        self.file_entry.pack(padx=10, pady=5)

        # Save button
        save_button = Button(self.dialog, text="Save", command=self.save_file)
        save_button.pack(pady=10)

    def on_select_extension(self, event):
        """Update the selected extension based on the user's choice in the Listbox."""
        selected = self.extension_listbox.curselection()
        if selected:
            self.extension.set(self.extension_listbox.get(selected))

    def save_file(self):
        """Open file dialog to select path, then save the file with the chosen name and extension."""
        file_path = filedialog.asksaveasfilename(
            initialfile=self.file_name.get(),
            initialdir=self.file_dir,
            defaultextension=self.extension.get(),
            filetypes=[(self.extension.get().upper(), f"*{self.extension.get()}")]
        )

        if file_path:
            # Ensure the file name includes the selected extension
            if not file_path.lower().endswith(self.extension.get()):
                file_path += self.extension.get()

            # Update the entry box with the chosen file path
            self.file_name.set(file_path)

            # Close the dialog window
            self.dialog.destroy()


# Example usage
if __name__ == "__main__":
    root = Tk()
    root.withdraw()  # Hide the root window

    save_dialog = SaveImageDialog(root, 'file_name', '/new_dir')
    save_dialog.open_save_dialog()

    root.mainloop()
