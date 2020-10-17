import tkinter as tk
import tkinter.ttk as ttk

from Utills.autocomplete_entry_words import AutocompleteEntryWords


class BankAccountFrame(tk.Frame):
    def __init__(self, root, db, **kw):
        super().__init__(**kw)
        self.db = db
        self.init_bank_account_frame(root)
        self.update_autocomplete()

    def init_bank_account_frame(self, root):
        padx = 5
        pady = 2
        self.bank_account_main_frame = tk.LabelFrame(root, text="Рахунок для оплати")
        self.bank_account_main_frame.pack(fill=tk.X, padx=padx)

        self.bank_account_name_frame = tk.Frame(self.bank_account_main_frame)
        self.bank_account_name_frame.pack(fill=tk.X)
        self.bank_account_name_label = tk.Label(self.bank_account_name_frame, text="Назва рахунку", width=14,
                                                anchor=tk.W)
        self.bank_account_name_label.pack(side=tk.LEFT, padx=padx, pady=pady)
        self.bank_account_name = AutocompleteEntryWords(self.bank_account_name_frame, completevalues=[])
        self.bank_account_name.pack(fill=tk.X, padx=padx, pady=pady)
        self.bank_account_name.bind('<Return>', self.set_bank_account_value)
        self.bank_account_name.bind('<Button-1>', self.set_bank_account_value)

        self.bank_account_value_frame = tk.Frame(self.bank_account_main_frame)
        self.bank_account_value_frame.pack(fill=tk.X)

        self.bank_account_value_label = tk.Label(self.bank_account_value_frame, text="Рахунок", width=14, anchor=tk.W)
        self.bank_account_value_label.pack(side=tk.LEFT, padx=padx, pady=pady)
        self.bank_account_value = ttk.Entry(self.bank_account_value_frame)
        self.bank_account_value.pack(fill=tk.X, padx=padx, pady=pady)

    def set_bank_account_value(self, event=None):
        name = self.bank_account_name.get()
        if name:
            value = self.db.get_bank_account_by_name(name)
            if value:
                self.bank_account_value.delete(0, tk.END)
                self.bank_account_value.insert(0, value[0])

    def update_autocomplete(self):
        bank_accounts_name = self.db.get_bank_account_list()
        self.bank_account_name.set_completion_list(bank_accounts_name)
