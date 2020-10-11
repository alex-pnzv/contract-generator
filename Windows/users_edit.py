import tkinter as tk
import tkinter.ttk as ttk

from Frames.user import UserFrame


class EditUsers(tk.Toplevel,UserFrame):
    def __init__(self,db,id,on_close, **kw):
        super().__init__(**kw)
        self.on_close = on_close
        self.id = id
        self.db = db
        self.init()
        self.insert_value(db,id)
        self.title("Редагування запису")
        self.grab_set()
        self.focus_set()
        self.minsize(480,290)

    def init(self):
        super().init_user_frame(self,self.db)
        self.edrpou.destroy()
        self.edrpou = ttk.Entry(self.edrpou_frame)
        self.edrpou.pack(fill=tk.X, padx=5)
        self.save_user_button.configure(text="Оновити", command=self.update_user)
        self.save_user_button.pack(side=tk.RIGHT, padx=5, pady=(0, 5))
        self.show_user_info_btn.pack_forget()
        self.hide_user_info_btn.pack_forget()
        self.user_frame.pack(fill=tk.X, padx=5,pady=5)

    def insert_value(self,db,id):
        row=db.get_user_by_id(id)
        self.name.insert(0,row[0])
        self.edrpou.insert(0,row[1])
        self.iban.insert(0,row[2])
        self.bank_mfo.insert(0,row[3])
        self.bank_name.insert(0,row[4])
        self.postal.insert(0,row[5])
        self.region.insert(0,row[6])
        self.district.insert(0,row[7])
        self.city.insert(0,row[8])
        self.street.insert(0,row[9])
        self.house.insert(0,row[10])
        self.telephone.insert(0,row[11])
        self.stamp_val.set(row[12])

    def update_user(self):
        name = self.name.get()
        edrpou = self.edrpou.get()
        iban = self.iban.get()
        bank_mfo = self.bank_mfo.get()
        bank_name = self.bank_name.get()
        postal = self.postal.get()
        region = self.region.get()
        district = self.district.get()
        city = self.city.get()
        street = self.street.get()
        house = self.house.get()
        telephone = self.telephone.get()
        stamp = self.stamp_val.get()
        self.db.update_user_by_id(self.id,name, edrpou,iban,bank_mfo,bank_name,postal,region,district,city,street,house,telephone,stamp)
        self.destroy()
        self.on_close()

