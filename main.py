import tkinter as tk
import tkinter.simpledialog as sd
from tkinter import Menu

from Frames.bank_account import BankAccountFrame
from Frames.contract import ContractFrame
from Frames.contract_term import ContractTerm
from Frames.contract_type import ContractType
from Frames.delivery_address import DeliveryAddressFrame
from Frames.delivery_time import DeliveryTimeFrame
from Frames.dk import DkFrame
from Frames.funding_source import FundingSourceFrame
from Frames.specification import Specification
from Frames.sum import SumFrame
from Frames.user import UserFrame
from Windows.address import Address
from Windows.bank_account import BankAccount
from Windows.templates import Templates
from Windows.users import Users
from Windows.dk import Dk
from database import DB
from Utills.utills import *


class Main(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Генератор договорів')
        self.minsize(600, 400)
        self.init_navbar()
        self.init_main()
        self.db = db
        self.protocol('WM_DELETE_WINDOW', self.save_before_close)
        self.bind_all("<Key>", self._on_key_release, "+")

    def init_navbar(self):
        navbar = Menu(self)
        directory_menu = Menu(navbar, tearoff=0)
        directory_menu.add_command(label="Контрагенти", command=self.open_user_db)
        directory_menu.add_separator()
        directory_menu.add_command(label="ДК", command=self.open_dk_db)
        directory_menu.add_separator()
        directory_menu.add_command(label="Адреси", command=self.open_address_db)
        directory_menu.add_separator()
        directory_menu.add_command(label="Рахунки", command=self.open_bank_account_db)

        file_menu = Menu(navbar, tearoff=0)
        file_menu.add_command(label="Новий договір", command=self.new_document)
        file_menu.add_command(label='Зберегти договір', command=self.save_contract)
        file_menu.add_command(label="Імпорт специфікації", command=self.import_spec)
        file_menu.add_command(label="Експорт специфікації", command=self.export_spec)
        file_menu.add_command(label="Експорт накладної", command=self.export_invoice)
        file_menu.add_separator()
        file_menu.add_command(label="Вихід", command=self.save_before_close)

        navbar.add_cascade(label='Файл', menu=file_menu)
        navbar.add_cascade(label="Довідники", menu=directory_menu)
        navbar.add_command(label="Шаблони", command=self.open_template_db)
        navbar.add_command(label="Справка", command=self.open_help)
        self.config(menu=navbar)

    def init_main(self):
        main_frame = tk.Frame(self)
        main_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        self.contract_type = ContractType(main_frame, self.change_contract_type, self.toggle_spec)
        self.contract_frame = ContractFrame(main_frame)

        self.user_frame = UserFrame(main_frame, db)
        valid_username = self.register(self.user_frame.check_user_name_value)
        self.user_frame.name.configure(validatecommand=(valid_username, "%P"))
        self.user_frame.hide_info()

        self.dk_frame = DkFrame(main_frame, db)
        self.delivery_address_frame = DeliveryAddressFrame(main_frame, db)
        self.bank_account_frame = BankAccountFrame(main_frame, db)

        self.contract_term_frame = ContractTerm(main_frame)
        valid_contract_date = self.register(self.contract_term_frame.check_contract_term_date)
        self.contract_term_frame.contract_term.configure(validatecommand=(valid_contract_date, "%P"))

        self.delivery_time_frame = DeliveryTimeFrame(main_frame)
        valid_delivery_date = self.register(self.delivery_time_frame.check_value)
        self.delivery_time_frame.delivery_time.configure(validatecommand=(valid_delivery_date, '%P'))

        self.funding_source_frame = FundingSourceFrame(main_frame)
        self.sum_frame = SumFrame(main_frame)

        self.spec_frame = Specification(text='Специфікація')
        # self.spec_frame.pack(side=tk.RIGHT,anchor=tk.N)
        # self.spec_frame.save_spec_btn.configure(command=self.export_spec)

        save_button = tk.Button(main_frame, text="Зберегти договір", command=self.save_contract)
        save_button.pack(side=tk.RIGHT, padx=10, pady=(0, 10), anchor=tk.N)

        save_template_button = tk.Button(main_frame, text='Зберегти шаблон', command=self.save_template)
        save_template_button.pack(side=tk.RIGHT, padx=0, pady=(0, 10), anchor=tk.N)

    def import_spec(self):
        try:
            data = load_spec()
            self.spec_frame.set_spec_values(data)
        except Exception as error:
            mb.showerror('Помилка',error)

    def export_spec(self):
        spec_data = self.spec_frame.get_spec_value()
        if spec_data:
            save_spec(spec_data, self.dk_frame.dk.get())

    def export_invoice(self):
        template_dict = self.get_entry_values()
        if template_dict:
            dirname = os.path.dirname(__file__)
            filename = os.path.join(dirname, 'templates\\nakladna.docx')
            print(filename)
            doc = DocxTemplate(filename)
            doc.render(template_dict)
            f = fd.asksaveasfile(mode='w', defaultextension=".docx", filetypes=(("DOCX", "*.docx"), ("All files", "*")))
            if f is None:  # asksaveasfile return `None` if dialog closed with "cancel".
                return
            name = f.name
            basename = os.path.basename(name)
            path = os.path.dirname(name)
            doc.save(path + "/" + basename)
            os.startfile(path)

    def change_contract_type(self):
        type = self.contract_type.contract_type_value.get()
        if type == "product":
            self.delivery_address_frame.delivery_place.pack(fill=tk.X, padx=5, after=self.dk_frame.dk_main_frame)
            self.delivery_time_frame.delivery_time_main_frame.pack(fill=tk.X, padx=5, pady=5,
                                                                   after=self.contract_term_frame.contract_term_main_frame)
        elif type == "service":
            self.delivery_address_frame.delivery_place.pack_forget()
            self.delivery_time_frame.delivery_time_main_frame.pack_forget()

    def toggle_spec(self, event=None):
        if self.contract_type.spec_value.get():
            self.spec_frame.pack(side=tk.LEFT, fill=tk.BOTH, anchor=tk.N, pady=5, padx=(0, 5))
        else:
            self.spec_frame.pack_forget()

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
        self.destroy()

    def get_entry_values(self):
        try:
            template_dict = {
                'user': str(self.user_frame.name.get()).strip(),
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
                'funding': str(self.funding_source_frame.get_funding_value()).strip(),
                'price_num': str(price_from_str(self.sum_frame.sum.get().strip())),
                'price_word': str(price_to_words(self.sum_frame.sum.get())).strip(),
                'initials_end': str(initials_end(self.user_frame.name.get())).strip(),
                'initials_start': str(initials_start(self.user_frame.name.get())).strip(),
                'capitalize_price': str(price_to_words(self.sum_frame.sum.get(), upper=True)).strip(),
                'stamp': self.user_frame.stamp_val.get(),
                'contract_term': str(month_to_text(self.contract_term_frame.contract_term.get())).strip(),
                'bank_account': self.bank_account_frame.get_values()
            }
            if self.contract_type.contract_type_value.get() == "product":
                template_dict.setdefault('delivery_time',
                                         str(month_to_text(self.delivery_time_frame.delivery_time.get())).strip())
            if self.contract_type.spec_value.get():
                template_dict.setdefault("spec_tbl", self.spec_frame.get_spec_value())
            return template_dict
        except InvalidUserName:
            mb.showerror("Помилка", "Невірно вказано ПІБ!")
        except InvalidDate:
            mb.showerror("Помилка", "Невірно вказана дата!")
        except InvalidSum:
            mb.showerror("Помилка", 'Невірно вказана сума!')
        except Exception as e:
            print(e)
            mb.showerror("Помилка", e)

    def save_contract(self):
        dirname = os.path.dirname(__file__)
        if self.contract_type.contract_type_value.get() == "product":
            filename = os.path.join(dirname, 'templates\\dogovir.docx')
        else:
            filename = os.path.join(dirname, 'templates\\dogovir_service.docx')
        print(filename)
        template_dict = self.get_entry_values()
        if template_dict:
            doc = DocxTemplate(filename)
            doc.render(template_dict)
            f = fd.asksaveasfile(mode='w', defaultextension=".docx", filetypes=(("DOCX", "*.docx"), ("All files", "*")))
            if f is None:  # asksaveasfile return `None` if dialog closed with "cancel".
                return
            name = f.name
            basename = os.path.basename(name)
            path = os.path.dirname(name)
            doc.save(path + "/" + basename)
            os.startfile(path)

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

    def open_help(self):
        os.startfile("info.chm")

    def new_document(self):
        result = mb.askyesno('Новий документ', 'Ви дійсно бажаєте створити новий документ?')
        if result:
            self.contract_type.contract_type_value.set('product')
            self.change_contract_type()
            self.contract_frame.contract.delete(0, tk.END)
            self.contract_type.spec_value.set(False)
            self.toggle_spec()
            self.spec_frame.destroy()
            self.spec_frame = Specification(text='Специфікація')

            self.user_frame.edrpou.delete(0, tk.END)
            self.user_frame.name.delete(0, tk.END)
            self.user_frame.iban.delete(0, tk.END)
            self.user_frame.postal.delete(0, tk.END)
            self.user_frame.region.delete(0, tk.END)
            self.user_frame.district.delete(0, tk.END)
            self.user_frame.city.delete(0, tk.END)
            self.user_frame.street.delete(0, tk.END)
            self.user_frame.house.delete(0, tk.END)
            self.user_frame.bank_name.delete(0, tk.END)
            self.user_frame.bank_mfo.delete(0, tk.END)
            self.user_frame.telephone.delete(0, tk.END)
            self.user_frame.stamp_val.set(True)

            self.dk_frame.dk.delete(0, tk.END)
            self.dk_frame.dk_desc.delete(1.0, tk.END)
            self.delivery_address_frame.institution.delete(0, tk.END)
            self.delivery_address_frame.institution_address.delete(0, tk.END)
            self.bank_account_frame.bank_account_name.delete(0, tk.END)
            self.bank_account_frame.bank_account_value.delete(0, tk.END)
            self.contract_term_frame.contract_term.delete(0, tk.END)
            self.delivery_time_frame.delivery_time.delete(0, tk.END)
            self.funding_source_frame.funding_value.set(1)
            self.sum_frame.sum.delete(0, tk.END)

    def load_template(self, template_id):
        row = self.db.get_template_by_id(template_id)
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

    def _on_key_release(self, event):
        ctrl = (event.state & 0x4) != 0
        if event.keycode == 88 and ctrl and event.keysym.lower() != "x":
            event.widget.event_generate("<<Cut>>")
        elif event.keycode == 86 and ctrl and event.keysym.lower() != "v":
            event.widget.event_generate("<<Paste>>")
        elif event.keycode == 67 and ctrl and event.keysym.lower() != "c":
            event.widget.event_generate("<<Copy>>")
        elif event.keycode == 65 and ctrl and event.keysym.lower() != "a":
            event.widget.event_generate("<<SelectAll>>")


if __name__ == '__main__':
    db = DB()
    app = Main()
    app.mainloop()
