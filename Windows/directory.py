import tkinter as tk
import tkinter.ttk as ttk

class Directory(tk.Toplevel):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.focus_set()
        self.grab_set()

        self.buttons_frame = tk.Frame(self)
        self.buttons_frame.pack(side=tk.TOP, fill=tk.X)

        self.add_button_pic = tk.PhotoImage(file='icons/add.png')
        self.edit_button_pic = tk.PhotoImage(file="icons/edit.png")
        self.remove_button_pic = tk.PhotoImage(file='icons/delete.png')

        self.add_button = tk.Button(self.buttons_frame, image=self.add_button_pic, width=20, height=20)
        self.add_button.pack(side=tk.LEFT, padx=(2, 0), pady=2)
        self.edit_button = tk.Button(self.buttons_frame, image=self.edit_button_pic, width=20, height=20)
        self.edit_button.pack(side=tk.LEFT, padx=2, pady=2)
        self.remove_button = tk.Button(self.buttons_frame, image=self.remove_button_pic, width=20, height=20)
        self.remove_button.pack(side=tk.LEFT, pady=2)

        self.search_entry = ttk.Entry(self.buttons_frame)
        self.search_entry.pack(side=tk.RIGHT, pady=2, padx=(0, 2))
        self.search_label = tk.Label(self.buttons_frame, text="Пошук:")
        self.search_label.pack(side=tk.RIGHT, pady=2)

