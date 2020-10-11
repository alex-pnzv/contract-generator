import os
import tkinter as tk
import tkinter.messagebox as mb
import tkinter.simpledialog as sd
from tkinter import Menu
from tkinter import filedialog as fd
from docxtpl import DocxTemplate

from Frames.bank_account import BankAccountFrame
from Frames.contract import ContractFrame
from Frames.contract_term import ContractTerm
from Frames.contract_type import ContractType
from Frames.delivery_address import DeliveryAddressFrame
from Frames.delivery_time import DeliveryTimeFrame
from Frames.dk import DkFrame
from Frames.funding_source import FundingSourceFrame
from Frames.sum import SumFrame
from Frames.user import UserFrame
from Windows.address import Address
from Windows.bank_account import BankAccount
from Windows.templates import Templates
from Windows.users import Users
from Windows.dk import Dk
from database import DB
from Utills.utills import *


class Main(tk.Frame):
    def __init__(self, root):
        super().__init__()
        self.init_navbar()
        self.init_main()
        self.db = db
        root.protocol('WM_DELETE_WINDOW', self.save_before_close)  # root is your root window

    def init_navbar(self):
        navbar = Menu(root)
        new_item = Menu(navbar, tearoff=0)
        new_item.add_command(label="Контрагенти", command=self.open_user_db)
        new_item.add_separator()
        new_item.add_command(label="ДК", command=self.open_dk_db)
        new_item.add_separator()
        new_item.add_command(label="Адреси", command=self.open_address_db)
        new_item.add_separator()
        new_item.add_command(label="Рахунки", command=self.open_bank_account_db)
        navbar.add_cascade(label="Довідники", menu=new_item)
        navbar.add_command(label="Шаблони", command=self.open_template_db)
        navbar.add_command(label="Справка")
        root.config(menu=navbar)

    def init_main(self):
        self.pack(fill=tk.BOTH, expand=True)

        self.contract_type = ContractType(self, self.change_contract_type)
        self.contract_frame = ContractFrame(self)

        self.user_frame = UserFrame(self, db)
        valid_username = self.register(self.user_frame.check_user_name_value)
        self.user_frame.name.configure(validatecommand=(valid_username, "%P"))

        self.user_frame.hide_info()

        self.dk_frame = DkFrame(self, db)
        self.delivery_address_frame = DeliveryAddressFrame(self, db)
        self.bank_account_frame = BankAccountFrame(self, db)

        self.contract_term_frame = ContractTerm(self)
        valid_contract_date = self.register(self.contract_term_frame.check_contract_term_date)
        self.contract_term_frame.contract_term.configure(validatecommand=(valid_contract_date, "%P"))

        self.delivery_time_frame = DeliveryTimeFrame(self)
        valid_delivery_date = self.register(self.delivery_time_frame.check_value)
        self.delivery_time_frame.delivery_time.configure(validatecommand=(valid_delivery_date, '%P'))

        self.funding_source_frame = FundingSourceFrame(self)
        self.sum_frame = SumFrame(self)

        save_button = tk.Button(root, text="Зберегти договір", command=self.save_docx)
        save_button.pack(side=tk.RIGHT, padx=10, pady=(0, 10))

        save_template_button = tk.Button(root, text='Зберегти шаблон', command=self.save_template)
        save_template_button.pack(side=tk.RIGHT, padx=0, pady=(0, 10))

    def change_contract_type(self):
        type = self.contract_type.contract_type_value.get()
        if type == "product":
            self.delivery_address_frame.delivery_place.pack(fill=tk.X, padx=5, after=self.dk_frame.dk_main_frame)
            self.delivery_time_frame.delivery_time_main_frame.pack(fill=tk.X, padx=5, pady=5,
                                                                   after=self.contract_term_frame.contract_term_main_frame)
        elif type == "service":
            self.delivery_address_frame.delivery_place.pack_forget()
            self.delivery_time_frame.delivery_time_main_frame.pack_forget()

    def save_user_if_not_exist(self):
        edrpou = self.user_frame.edrpou.get()
        rows = self.db.get_user_by_edrpou(edrpou)
        if not rows:
            self.user_frame.save_user()

    def save_before_close(self):
        # check if saving
        edrpou = self.user_frame.edrpou.get()
        if edrpou:
            rows = self.db.get_user_by_edrpou(edrpou)
            if not rows:
                result = mb.askyesno("Додати в довідник", "Зберегти контрагента в довідник?")
                if result:
                    self.user_frame.save_user()
        # if not:
        root.destroy()

    def save_docx(self):
        # Prepare the data...
        dirname = os.path.dirname(__file__)
        if self.contract_type.contract_type_value.get() == "product":
            filename = os.path.join(dirname, 'templates\\dogovir.docx')
        else:
            filename = os.path.join(dirname, 'templates\\dogovir_service.docx')
        try:
            doc = DocxTemplate(filename)
            doc.render(
                {'user': str(self.user_frame.name.get()).strip(),
                 'edrpou': str(self.user_frame.edrpou.get()).strip(),
                 'iban': str(self.user_frame.iban.get()).strip(),
                 'bank_mfo': str(self.user_frame.bank_mfo.get()).strip(),
                 'bank_name': str(self.user_frame.bank_name.get()).strip(),
                 'postal': str(self.user_frame.postal.get()).strip(),
                 'region': str(self.user_frame.region.get()).strip(),
                 'district': str(self.user_frame.district.get()).strip(),
                 'city': str(self.user_frame.city.get()).strip(),
                 'street': str(self.user_frame.street.get()).strip(),
                 'house': str(self.user_frame.house.get()).strip(),
                 'telephone': str(self.user_frame.telephone.get()).strip(),
                 'contract_subject': str(self.contract_frame.contract.get()).strip(),
                 'DK_num': str(self.dk_frame.dk.get()).strip(),
                 'DK_description': str(self.dk_frame.dk_desc.get(1.0, tk.END)).strip(),
                 'institution_name': str(self.delivery_address_frame.institution.get()).strip(),
                 'institution_address': str(self.delivery_address_frame.institution_address.get()).strip(),
                 'delivery_time': str(month_to_text(self.delivery_time_frame.delivery_time.get())).strip(),
                 'funding': str(self.funding_source_frame.get_funding_value()).strip(),
                 'price_num': str(self.sum_frame.sum.get()).strip(),
                 'price_word': str(price_to_words(self.sum_frame.sum.get())).strip(),
                 'initials_end': str(initials_end(self.user_frame.name.get())).strip(),
                 'initials_start': str(initials_start(self.user_frame.name.get())).strip(),
                 'capitalize_price': str(price_to_words(self.sum_frame.sum.get(), upper=True)).strip(),
                 'stamp': str(self.user_frame.stamp_val.get()).strip(),
                 'contract_term': str(month_to_text(self.contract_term_frame.contract_term.get())).strip(),
                 'bank_account': str(self.bank_account_frame.bank_account_value.get()).strip()
                 }
            )

            f = fd.asksaveasfile(mode='w', defaultextension=".docx", filetypes=(("DOCX", "*.docx"), ("All files", "*")))
            if f is None:  # asksaveasfile return `None` if dialog closed with "cancel".
                return

            name = f.name
            basename = os.path.basename(name)
            path = os.path.dirname(name)
            print(path)
            print(basename)

            doc.save(path + "/" + basename)
            os.startfile(path)

        except InvalidUserName:
            mb.showerror("Помилка", "Невірно вказано ПІБ!")
        except InvalidDate:
            mb.showerror("Помилка", "Невірно вказана дата!")
        except InvalidSum:
            mb.showerror("Помилка", 'Невірно вказана сума!')
        except Exception as e:
            print(e)
            mb.showerror("Помилка", e)

    def open_user_db(self):
        Users(self, db)

    def open_dk_db(self):
        Dk(self, db)

    def open_address_db(self):
        Address(self, db)

    def open_bank_account_db(self):
        BankAccount(self, db)

    def open_template_db(self):
        Templates(db, self.load_template)

    def load_template(self, id):
        row = self.db.get_template_by_id(id)
        if row:
            self.contract_type.contract_type_value.set(row[2])
            self.change_contract_type()
            self.contract_frame.contract.delete(0, tk.END)
            self.contract_frame.contract.insert(0, row[3])
            self.user_frame.edrpou.delete(0, tk.END)
            self.user_frame.edrpou.insert(0, row[4])
            self.user_frame.find_user_by_edrpou()
            self.dk_frame.dk.delete(0, tk.END)
            self.dk_frame.dk.insert(0, row[5])
            self.dk_frame.set_dk_description()
            self.delivery_address_frame.institution.delete(0, tk.END)
            self.delivery_address_frame.institution.insert(0, row[6])
            self.delivery_address_frame.set_delivery_address()
            self.delivery_address_frame.institution.unpost_listbox()
            self.bank_account_frame.bank_account_name.delete(0, tk.END)
            self.bank_account_frame.bank_account_name.insert(0, row[7])
            self.bank_account_frame.set_bank_account_value()
            self.contract_term_frame.contract_term.delete(0, tk.END)
            self.contract_term_frame.contract_term.insert(0, row[8])
            self.delivery_time_frame.delivery_time.delete(0, tk.END)
            self.delivery_time_frame.delivery_time.insert(0, row[9])
            self.funding_source_frame.set_funding_value(row[10])
            self.sum_frame.sum.delete(0, tk.END)
            self.sum_frame.sum.insert(0, row[11])

    def save_template(self):
        template_name = sd.askstring("Збереження шаблону", "Введіть назву шаблону")
        if template_name:
            self.db.set_template(template_name,
                                 self.contract_type.contract_type_value.get(),
                                 self.contract_frame.contract.get(),
                                 self.user_frame.edrpou.get(),
                                 self.dk_frame.dk.get(),
                                 self.delivery_address_frame.institution.get(),
                                 self.bank_account_frame.bank_account_name.get(),
                                 self.contract_term_frame.contract_term.get(),
                                 self.delivery_time_frame.delivery_time.get(),
                                 self.funding_source_frame.get_funding_value(),
                                 self.sum_frame.sum.get()
                                 )


if __name__ == '__main__':
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.minsize(600, 100)
    root.title('Генератор договорів')
    # root.geometry('600x640+300+200')
    root.resizable(True, True)
    root.mainloop()
