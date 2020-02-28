import tkinter as tk
from tkinter import ttk


class ScrollableFrame(ttk.Frame):
    """
    Scrollable Frame
    """
    def __init__(self, container, *args, **kwargs):
        """
        Constructs a Scrollable Frame
        :param container: The parent frame
        :param args: endless amount of arguments
        :param kwargs: keyword arguments
        """
        super().__init__(container, *args, **kwargs)

        # Create canvas
        canvas = tk.Canvas(self, height=410, width=465,bd=0, highlightthickness=0, relief='ridge')
        canvas.config(bg='#f7f8f9')

        # Create scrollbar
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        # Configure scroll region on canvas
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        # Set scrollable_frame frame to canvas
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
