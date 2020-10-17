import tkinter as tk
from Utills.autocomplete_entry import AutocompleteEntry


class DkFrame:
    def __init__(self,root,db):
        self.db = db
        self.init_dk_frame(root)
        self.update_autocomplete_dk_list()

    def init_dk_frame(self,root):
        padx = 5
        pady = 2

        self.dk_main_frame = tk.LabelFrame(root, text="ДК 021:2015")
        self.dk_main_frame.pack(fill=tk.X,padx=padx)
        dk_frame = tk.Frame(self.dk_main_frame)
        dk_frame.pack(fill=tk.X)
        dk_label = tk.Label(dk_frame, text="Номер ДК", width=14, anchor=tk.W)
        dk_label.pack(side=tk.LEFT,padx=padx,pady=pady)
        self.dk = AutocompleteEntry(dk_frame,completevalues=[])
        self.dk.pack(fill=tk.X,padx=padx,pady=pady)

        self.dk.bind('<Return>', self.set_dk_description)
        self.dk.bind('<Button-1>',self.set_dk_description)

        dk_desc_frame = tk.Frame(self.dk_main_frame)
        dk_desc_frame.pack(fill=tk.X)
        dk_desc_label = tk.Label(dk_desc_frame, text="Опис", width=14, anchor=tk.W)
        dk_desc_label.pack(side=tk.LEFT,padx=padx,pady=pady)
        self.dk_desc = tk.Text(dk_desc_frame,width=25, height=2)
        self.dk_desc.pack(fill=tk.X,padx=padx,pady=pady)
        self.dk_desc.configure(font=('TkTextFont ',9))

        save_dk = tk.Frame(self.dk_main_frame)
        save_dk.pack(fill=tk.X)
        self.save_dk_button = tk.Button(save_dk)

    def set_dk_description(self, event=None):
        dk_code = str(self.dk.get())
        if dk_code:
            dk_desc = self.db.get_dk_desc_by_code(dk_code)
            if dk_desc:
                self.dk_desc.delete(1.0, tk.END)
                self.dk_desc.insert(1.0, dk_desc[0])

    def update_autocomplete_dk_list(self):
        dk_completion_list = self.db.get_dk_code_list()
        self.dk.set_completion_list(dk_completion_list)