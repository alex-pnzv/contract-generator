import tkinter as tk
import tkinter.ttk as ttk
from Utills.multiple_autocomplete_entry import MultipleAutocompleteEntry


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
        self.bank_account_name = MultipleAutocompleteEntry(self.bank_account_name_frame, completevalues=[])
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
        ba_name_entry_value = self.bank_account_name.get()
        if ba_name_entry_value:
            bank_account_names = [n.strip() for n in ba_name_entry_value.split(',')]
            values = self.db.get_bank_account_by_name(bank_account_names)
            result = [val[0] for val in values]
            if values:
                bank_accounts = ', '.join(result)
                self.bank_account_value.delete(0, tk.END)
                self.bank_account_value.insert(0, bank_accounts)

    def update_autocomplete(self):
        bank_accounts_name = self.db.get_bank_account_list()
        self.bank_account_name.set_completion_list(bank_accounts_name)

    def get_values(self):
        entry_value = self.bank_account_value.get()
        result = [value.strip() for value in entry_value.split(',')]
        return result
