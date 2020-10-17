import tkinter as tk

from Frames.delivery_address import DeliveryAddressFrame


class AddAddress(tk.Toplevel, DeliveryAddressFrame):
    def __init__(self, db, on_close, **kw):
        super().__init__(**kw)
        self.on_close = on_close
        self.db = db
        self.title('Новий запис')
        self.minsize(600, 110)
        self.grab_set()
        self.focus_set()
        self.init_add_address()

    def init_add_address(self):
        super().init_frame(self)
        self.save_delivery_place.configure(text='Додати в довідник', command=self.add_new_address)
        self.save_delivery_place.pack(side=tk.RIGHT, padx=5, pady=(0, 5))

    def add_new_address(self):
        institution_name = self.institution.get()
        institution_address = self.institution_address.get()
        self.db.set_address(institution_name, institution_address)
        self.destroy()
        self.on_close()
