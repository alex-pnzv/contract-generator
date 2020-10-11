import tkinter as tk
import  tkinter.ttk as ttk
from Frames.user import UserFrame


class UserAdd(tk.Toplevel,UserFrame):
    def __init__(self,db,on_close, **kw):
        super().__init__(**kw)
        self.on_close = on_close
        self.title("Новий запис")
        self.minsize(480,290)
        self.grab_set()
        self.focus_set()
        super().init_user_frame(self,db)
        self.edrpou.destroy()
        self.edrpou = ttk.Entry(self.edrpou_frame)
        self.edrpou.pack(fill=tk.X, padx=5)
        self.show_user_info_btn.pack_forget()
        self.hide_user_info_btn.pack_forget()
        self.user_frame.pack(fill=tk.X, padx=5, pady=5)
        self.save_user_button.configure(command=self.save_user)
        self.save_user_button.pack(side=tk.RIGHT, padx=5, pady=(0,5))

    def save_user(self):
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

        self.db.set_users(name, edrpou,iban,bank_mfo,bank_name,postal,region,district,city,street,house,telephone,stamp)
        self.destroy()
        self.on_close()

