import tkinter as tk
import tkinter.ttk as ttk
from icons import icons


class ContractTerm:
    def __init__(self, root):
        self.contract_term_main_frame = tk.Frame(root)
        self.contract_term_main_frame.pack(fill=tk.X, padx=5)

        contract_term_label = tk.Label(self.contract_term_main_frame, width=14, text="Термін договору", anchor=tk.W)
        contract_term_label.pack(side=tk.LEFT, padx=5, pady=(5, 0))

        self.contract_term = ttk.Entry(self.contract_term_main_frame, validate="focusout")
        self.contract_term.pack(fill=tk.X, padx=7, pady=(5, 0))

        self.error_photo = tk.PhotoImage(data=icons.warning)
        self.error_label = tk.Label(self.contract_term_main_frame, image=self.error_photo)

    def check_contract_term_date(self, text: str):
        if len(text.split(',')) == 3:
            date = text.split(',')
            if int(date[1]) > 12:
                self.contract_term.pack(side=tk.LEFT, fill=tk.X, padx=(7, 0), pady=(5, 0), expand=True)
                self.error_label.pack(side=tk.RIGHT)
                return False
            self.error_label.pack_forget()
            self.contract_term.pack(side=tk.LEFT, fill=tk.X, padx=7, pady=(5, 0), expand=True)
            return True
        elif len(text.split('.')) == 3:
            date = text.split('.')
            if int(date[1]) > 12:
                self.contract_term.pack(side=tk.LEFT, fill=tk.X, padx=(7, 0), pady=(5, 0), expand=True)
                self.error_label.pack(side=tk.RIGHT)
                return False
            self.contract_term.pack(side=tk.LEFT, fill=tk.X, padx=7, pady=(5, 0), expand=True)
            self.error_label.pack_forget()
            return True
        else:
            self.contract_term.pack(side=tk.LEFT, fill=tk.X, padx=(7, 0), pady=(5, 0), expand=True)
            self.error_label.pack(side=tk.RIGHT)
            return False
