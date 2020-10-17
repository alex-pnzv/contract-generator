import tkinter as tk

from Frames.dk import DkFrame


class DkAdd(tk.Toplevel, DkFrame):
    def __init__(self, db, on_close, **kw):
        super().__init__(**kw)
        self.on_close = on_close
        self.db = db
        self.minsize(600, 120)
        self.title('Новий запис')
        self.grab_set()
        self.focus_set()
        self.init_dk_add()

    def init_dk_add(self):
        super().init_dk_frame(self)
        self.save_dk_button.configure(text='Додати в довідник', command=self.save_dk)
        self.save_dk_button.pack(side=tk.RIGHT, padx=5, pady=(2, 5))

    def save_dk(self):
        code = self.dk.get()
        desc = self.dk_desc.get(1.0, tk.END)
        self.db.set_dk(code, desc)
        self.destroy()
        self.on_close()
