from tkinter import Frame


class BaseScreen(Frame):
  def __init__(self, parent):
    super().__init__(parent)
    self.configure(bg='#F3F3E0')
    self.thumbnail_size = (300, 300)
