import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as mb

from Utills.autocomplete_entry_words import AutocompleteEntryWords
from icons import icons


class UserFrame:
    def __init__(self, root, db):
        self.init_user_frame(root, db)
        self.update_autocomplete_edrpou_list()

    def init_user_frame(self, root, db):
        width = 14
        padx = 5
        pady = 2
        self.db = db

        self.user_frame = tk.LabelFrame(root, text="Контрагент")
        self.user_frame.pack(fill=tk.X, padx=padx)

        # Поле ЄДРПОУ
        self.edrpou_frame = tk.Frame(self.user_frame)
        self.edrpou_frame.pack(fill=tk.X)
        edrpou_label = tk.Label(self.edrpou_frame, text="ЄДРПОУ", width=width, anchor=tk.W)
        edrpou_label.pack(side=tk.LEFT, padx=padx, pady=pady)
        self.edrpou = AutocompleteEntryWords(self.edrpou_frame, completevalues=[])

        self.edrpou.pack(fill=tk.X, side=tk.LEFT, padx=(padx, 0), pady=pady, expand=True)
        self.edrpou.bind("<Return>", self.find_user_by_edrpou)
        self.edrpou.bind("<Button-1>", self.find_user_by_edrpou)

        # Поле Имя
        name_frame = tk.Frame(self.user_frame)
        name_frame.pack(fill=tk.X, pady=(0, 5))
        name_label = tk.Label(name_frame, text="Ім'я", width=width, anchor=tk.W)
        name_label.pack(side=tk.LEFT, padx=padx, pady=pady)
        self.name = ttk.Entry(name_frame, validate="focusout")
        self.name.pack(fill=tk.X, padx=padx, pady=pady)
        self.error_photo = tk.PhotoImage(data=icons.warning)
        self.error_label = tk.Label(name_frame, image=self.error_photo)

        # Поле IBAN
        self.iban_frame = tk.Frame(self.user_frame)
        self.iban_frame.pack(fill=tk.X)
        iban_label = tk.Label(self.iban_frame, text="IBAN", width=width, anchor=tk.W)
        iban_label.pack(side=tk.LEFT, padx=padx, pady=pady)
        self.iban = ttk.Entry(self.iban_frame)
        self.iban.pack(fill=tk.X, padx=padx, pady=pady)

        # Поле Банк
        self.bank_frame = tk.Frame(self.user_frame)
        self.bank_frame.pack(fill=tk.X)
        bank_label = tk.Label(self.bank_frame, text="Банк", width=width, anchor=tk.W)
        bank_label.grid(row=0, column=0, padx=padx, pady=pady)
        bank_mfo_label = tk.Label(self.bank_frame, width=5, text="МФО")
        bank_mfo_label.grid(row=0, column=1)
        self.bank_mfo = ttk.Entry(self.bank_frame)
        self.bank_mfo.grid(row=0, column=2, padx=padx, pady=pady, sticky="ew")
        bank_name_label = tk.Label(self.bank_frame, width=5, text="Назва")
        bank_name_label.grid(row=0, column=3)
        self.bank_name = ttk.Entry(self.bank_frame)
        self.bank_name.grid(row=0, column=4, padx=padx, pady=pady, sticky="ew")

        self.bank_frame.grid_rowconfigure(2, weight=1)
        self.bank_frame.grid_columnconfigure(2, weight=1)
        self.bank_frame.grid_rowconfigure(4, weight=1)
        self.bank_frame.grid_columnconfigure(4, weight=1)

        # Поле Адресс
        self.address_frame = tk.Frame(self.user_frame)
        self.address_frame.pack(fill=tk.X)
        address_label = tk.Label(self.address_frame, text="Адреса", width=width, anchor=tk.W)
        address_label.grid(row=0, column=0, padx=padx, pady=pady)
        postal_label = tk.Label(self.address_frame, text="індекс")
        postal_label.grid(row=0, column=1)
        self.postal = ttk.Entry(self.address_frame)
        self.postal.grid(row=0, column=2, padx=padx, pady=pady, sticky="ew")
        region_label = tk.Label(self.address_frame, text="обл.")
        region_label.grid(row=0, column=3)
        self.region = ttk.Entry(self.address_frame)
        self.region.grid(row=0, column=4, padx=padx, pady=pady, sticky="ew")
        district_label = tk.Label(self.address_frame, text="район")
        district_label.grid(row=1, column=1)
        self.district = ttk.Entry(self.address_frame)
        self.district.grid(row=1, column=2, padx=padx, pady=pady, sticky="ew")
        city_label = tk.Label(self.address_frame, text="місто")
        city_label.grid(row=1, column=3)
        self.city = ttk.Entry(self.address_frame)
        self.city.grid(row=1, column=4, padx=padx, pady=pady, sticky="ew")
        street_label = tk.Label(self.address_frame, width=5, text="вул.")
        street_label.grid(row=3, column=1)
        self.street = ttk.Entry(self.address_frame)
        self.street.grid(row=3, column=2, padx=padx, pady=pady, sticky="ew")
        house_label = tk.Label(self.address_frame, width=5, text="буд.")
        house_label.grid(row=3, column=3)
        self.house = ttk.Entry(self.address_frame)
        self.house.grid(row=3, column=4, padx=padx, pady=pady, sticky="ew")

        self.address_frame.grid_rowconfigure(2, weight=1)
        self.address_frame.grid_columnconfigure(2, weight=1)
        self.address_frame.grid_rowconfigure(4, weight=1)
        self.address_frame.grid_columnconfigure(4, weight=1)

        # Поле телефон
        self.telephone_frame = tk.Frame(self.user_frame)
        self.telephone_frame.pack(fill=tk.X)
        telephone_label = tk.Label(self.telephone_frame, text="Телефон", width=width, anchor=tk.W)
        telephone_label.pack(side=tk.LEFT, padx=padx, pady=pady)
        self.telephone = ttk.Entry(self.telephone_frame)
        self.telephone.pack(fill=tk.X, padx=padx, pady=pady)

        # Поле Наявність печатки
        self.stamp_val = tk.BooleanVar()
        self.stamp_frame = tk.Frame(self.user_frame)
        self.stamp_frame.pack(fill=tk.X)
        stamp_label = tk.Label(self.stamp_frame, text="Наявність печатки")
        stamp_label.pack(side=tk.LEFT, padx=padx, pady=pady)
        self.stamp1 = tk.Radiobutton(self.stamp_frame, variable=self.stamp_val, value=True, text="Має печатку")
        self.stamp1.pack(side=tk.LEFT)
        self.stamp2 = tk.Radiobutton(self.stamp_frame, variable=self.stamp_val, value=False, text='Немає печатки')
        self.stamp2.pack(side=tk.LEFT)
        self.stamp_val.set(True)

        # Кнопка сохранения пользователя в БД
        self.save_user_btn_frame = tk.Frame(self.user_frame)
        self.save_user_btn_frame.pack(fill=tk.X)
        self.save_user_button = tk.Button(self.save_user_btn_frame, text="Додати в довідник", command=self.save_user)
        # self.save_user_button.pack(side=tk.RIGHT, padx=padx, pady=(0,5))

        self.null_image = tk.PhotoImage(width=30, height=30)
        self.less_image = tk.PhotoImage(data=icons.less)
        self.hide_user_info_btn = tk.Button(self.edrpou_frame, command=self.hide_info, width="17", height="17",
                                            image=self.less_image,
                                            highlightthickness=0, padx=0, pady=0)
        self.hide_user_info_btn.pack(side=tk.RIGHT, padx=padx, pady=(0, 5))

        self.more_image = tk.PhotoImage(data=icons.more)
        self.show_user_info_btn = tk.Button(self.edrpou_frame, command=self.show_info, width="17", height="17",
                                            image=self.more_image, compound="center", highlightthickness=0, padx=0,
                                            pady=0)
        self.show_user_info_btn.pack(side=tk.LEFT, padx=(0, 10))
        # END ---------Контрагент-----------

    def update_autocomplete_edrpou_list(self):
        edrpou_list = self.db.get_edrpou_list()
        self.edrpou.set_completion_list(edrpou_list)

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
        try:
            self.db.set_users(name, edrpou, iban, bank_mfo, bank_name, postal, region, district, city, street, house,
                              telephone, stamp)
            mb.showinfo("Інфо", "Успішно додано в довідник")
        except Exception as e:
            mb.showerror("Помилка", e)

    def find_user_by_edrpou(self, event=None):
        edrpou = str(self.edrpou.get())
        if edrpou:
            row = self.db.get_user_by_edrpou(edrpou)
            if row:
                self.name.delete(0, tk.END)
                self.name.insert(0, row[0])
                self.edrpou.delete(0, tk.END)
                self.edrpou.insert(0, row[1])
                self.iban.delete(0, tk.END)
                self.iban.insert(0, row[2])
                self.bank_mfo.delete(0, tk.END)
                self.bank_mfo.insert(0, row[3])
                self.bank_name.delete(0, tk.END)
                self.bank_name.insert(0, row[4])
                self.postal.delete(0, tk.END)
                self.postal.insert(0, row[5])
                self.region.delete(0, tk.END)
                self.region.insert(0, row[6])
                self.district.delete(0, tk.END)
                self.district.insert(0, row[7])
                self.city.delete(0, tk.END)
                self.city.insert(0, row[8])
                self.street.delete(0, tk.END)
                self.street.insert(0, row[9])
                self.house.delete(0, tk.END)
                self.house.insert(0, row[10])
                self.telephone.delete(0, tk.END)
                self.telephone.insert(0, row[11])
                self.stamp_val.set(row[12])

    def hide_info(self):
        self.iban_frame.pack_forget()
        self.address_frame.pack_forget()
        self.bank_frame.pack_forget()
        self.telephone_frame.pack_forget()
        self.save_user_btn_frame.pack_forget()
        self.hide_user_info_btn.pack_forget()
        self.stamp_frame.pack_forget()
        self.show_user_info_btn.pack(side=tk.LEFT, padx=(0, 5))

    def show_info(self):
        self.iban_frame.pack(fill=tk.X)
        self.address_frame.pack(fill=tk.X)
        self.bank_frame.pack(fill=tk.X)
        self.telephone_frame.pack(fill=tk.X)
        self.stamp_frame.pack(fill=tk.X)
        self.save_user_btn_frame.pack(fill=tk.X)
        self.show_user_info_btn.pack_forget()

        self.hide_user_info_btn.pack(side=tk.LEFT, padx=(0, 5))

    def check_user_name_value(self, text: str):
        if len(text.split(' ')) == 3:
            self.error_label.pack_forget()
            self.name.pack(side=tk.LEFT, fill=tk.X, padx=5, pady=2, expand=True)
            return True
        else:
            self.name.pack(side=tk.LEFT, fill=tk.X, padx=(5, 0), pady=2, expand=True)
            self.error_label.pack(side=tk.RIGHT)
            return False
