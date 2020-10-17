import tkinter as tk
import tkinter.ttk as ttk
from Utills.combobox_autocomplete import ComboboxAutocomplete


class DeliveryAddressFrame():
    def __init__(self, root, db):
        self.db = db
        self.init_frame(root)
        self.update_autocomplete_address_list()

    def init_frame(self, root):
        padx = 5
        pady = 2

        self.delivery_place = tk.LabelFrame(root, text="Місце поставки")
        self.delivery_place.pack(fill=tk.X, padx=padx)

        self.institution_frame = tk.Frame(self.delivery_place)
        self.institution_frame.pack(fill=tk.X)
        institution_label = tk.Label(self.institution_frame, text="Назва закладу", width=14, anchor=tk.W)
        institution_label.pack(side=tk.LEFT, padx=padx, pady=pady)
        self.institution = ComboboxAutocomplete(self.institution_frame, [], callback=self.set_delivery_address,
                                                listbox_height=4)

        self.institution.pack(fill=tk.X, padx=padx, pady=pady)

        institution_adress_frame = tk.Frame(self.delivery_place)
        institution_adress_frame.pack(fill=tk.X)
        institution_address_label = tk.Label(institution_adress_frame, text="Адреса", width=14, anchor=tk.W)
        institution_address_label.pack(side=tk.LEFT, padx=padx, pady=pady)
        self.institution_address = ttk.Entry(institution_adress_frame)
        self.institution_address.pack(fill=tk.X, padx=padx, pady=pady)

        self.save_delivery_place = tk.Button(self.delivery_place)

    def set_delivery_address(self):
        institution_name = self.institution.get()
        if institution_name:
            address = self.db.get_delivery_address_by_name(institution_name)
            if address:
                self.institution_address.delete(0, tk.END)
                self.institution_address.insert(0, address[0])

    def update_autocomplete_address_list(self):
        institution_list = self.db.get_institution_name_list()
        if institution_list:
            self.institution.set_list_of_items(institution_list)
