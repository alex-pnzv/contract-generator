import tkinter as tk

from Frames.bank_account import BankAccountFrame


class EditBankAccount(tk.Toplevel,BankAccountFrame):
    def __init__(self,db,id,onclosecommand, **kw):
        super().__init__(**kw)
        self.title('Редагування запису')
        self.on_close_command = onclosecommand
        self.db = db
        self.bank_account_id = id
        self.focus_set()
        self.grab_set()
        self.init_frame()
        self.get_value()
        self.minsize(350,0)

    def init_frame(self):
        super().init_bank_account_frame(self)
        self.update_button =tk.Button(self.bank_account_main_frame, text='Оновити',command=self._update)
        self.update_button.pack(side=tk.RIGHT,padx=5,pady=5)
        self.bank_account_main_frame.pack(pady=(0,5))

    def get_value(self):
        row = self.db.get_bank_account_by_id(self.bank_account_id)
        self.bank_account_name.insert(0,row[0])
        self.bank_account_value.insert(0,row[1])

    def _update(self):
        name = self.bank_account_name.get()
        value = self.bank_account_value.get()
        self.db.update_bank_account_by_id(self.bank_account_id,name,value)
        self.destroy()
        self.on_close_command()


