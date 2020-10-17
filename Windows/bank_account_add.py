import tkinter as tk

from Frames.bank_account import BankAccountFrame


class AddBankAccount(tk.Toplevel, BankAccountFrame):
    def __init__(self, db, onclosecommand, **kw):
        super().__init__(**kw)
        self.title("Новий запис")
        self.on_close_command = onclosecommand
        self.focus_set()
        self.grab_set()
        self.init_frame()
        self.db = db
        self.minsize(350, 0)

    def init_frame(self):
        super().init_bank_account_frame(self)
        self.save_button = tk.Button(self.bank_account_main_frame, text="Додати в довідник", command=self._save)
        self.save_button.pack(side=tk.RIGHT, padx=5, pady=5)
        self.bank_account_main_frame.pack(pady=(0, 5))

    def _save(self):
        name = self.bank_account_name.get()
        value = self.bank_account_value.get()
        self.db.set_bank_account(name, value)
        self.destroy()
        self.on_close_command()
