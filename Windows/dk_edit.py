import tkinter as tk

from Frames.dk import DkFrame


class EditDk(tk.Toplevel, DkFrame):
    def __init__(self, db, dk_id, on_close, **kw):
        super().__init__(**kw)
        self.db = db
        self.id = dk_id
        self.on_close = on_close
        self.init()
        self.insert_value()

    def init(self):
        self.title("Редагування запису")
        self.focus_set()
        self.grab_set()
        self.minsize(600, 120)

        super().init_dk_frame(self)
        self.save_dk_button.configure(text='Оновити', command=self.update_dk)
        self.save_dk_button.pack(side=tk.RIGHT, padx=5, pady=(2, 5))

    def update_dk(self):
        code = self.dk.get()
        desc = self.dk_desc.get(1.0, tk.END)
        self.db.update_dk_by_id(self.id, code, desc)
        self.destroy()
        self.on_close()

    def insert_value(self):
        row = self.db.get_dk_by_id(self.id)
        self.dk.insert(0, row[0])
        self.dk_desc.insert(1.0, row[1])
