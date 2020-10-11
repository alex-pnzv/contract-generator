from Frames import delivery_address as d
import tkinter as tk


class EditAddress(tk.Toplevel,d.DeliveryAddressFrame):
    def __init__(self,root,db,id=None, on_close=None, **kw):
        super().__init__(root,**kw)
        self.id = id
        self.db = db
        self.on_close = on_close
        self.init_edit_frame()


    def init_edit_frame(self):
        self.title('Редагування запису')
        self.focus_set()
        self.grab_set()
        self.minsize(600,110)


        super().init_frame(self)
        self.institution.destroy()
        self.institution = tk.Entry(self.institution_frame)
        self.institution.pack(fill=tk.X, padx=5,pady=5)
        self.save_delivery_place.pack(side=tk.RIGHT, padx=5, pady=(0, 5))


        self.save_delivery_place.configure(text="Оновити",command=self.update_address)
        row = self.db.get_address_by_id(self.id)
        self.institution.delete(0, tk.END)
        self.institution.insert(0, row[0])
        self.institution_address.delete(0, tk.END)
        self.institution_address.insert(0, row[1])

    def update_address(self):
        institution_name = self.institution.get()
        institution_adddress = self.institution_address.get()
        try:
            self.db.update_address_by_id(self.id,institution_name,institution_adddress)
            self.destroy()
            self.on_close()
        except Exception as e:
            pass