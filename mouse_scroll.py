import platform

def bind_mouse_scroll(widget):
    # Define platform-specific mouse wheel scrolling behavior
    def _on_mouse_wheel(event):
        # Windows and Linux (where delta is positive/negative for up/down)
        if platform.system() == "Windows" or platform.system() == "Linux":
            widget.yview_scroll(-1 * (event.delta // 120), "units")
        elif platform.system() == "Darwin":  # macOS
            # macOS uses Button-4 and Button-5 for scroll events
            if event.num == 4:  # Scroll up
                widget.yview_scroll(-1, "units")
            elif event.num == 5:  # Scroll down
                widget.yview_scroll(1, "units")

    # Bind appropriate event to the widget for vertical scrolling
    if platform.system() == "Windows" or platform.system() == "Linux":
        # activate mousewheel when it is over the widget
        widget.bind('<Enter>', lambda e: widget.bind('<MouseWheel>',_on_mouse_wheel))
        widget.bind('<Leave>', lambda e: widget.unbind('<MouseWheel>'))
    elif platform.system() == "Darwin":  # macOS
        # For macOS, bind Button-4 and Button-5 events
        widget.bind('<Enter>', lambda e: (widget.bind('<Button-4>', _on_mouse_wheel),
                                          widget.bind('<Button-5>', _on_mouse_wheel)))
        # Unbind when the mouse leaves the widget
        widget.bind('<Leave>', lambda e: (widget.unbind('<Button-4>'),
                                          widget.unbind('<Button-5>')))
