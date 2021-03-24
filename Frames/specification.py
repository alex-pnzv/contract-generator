import decimal
import tkinter as tk
import tkinter.ttk as ttk
from decimal import Decimal, ROUND_HALF_UP

from Utills.utills import save_spec, price_from_str
from Utills.autocomplete_entry_words import AutocompleteEntryWords


class Specification(tk.LabelFrame):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.MIN_NUMBER_POSITION = 1
        self.MAX_NUMBER_POSITION = 30
        self.entries = []
        self.measurement_autocomplete = []

        self.count_spec_position_frame = tk.Frame(self)
        self.count_spec_position_frame.grid()
        self.count_spec_position_label = tk.Label(self.count_spec_position_frame, text='Кількість позицій', width=14)
        self.count_spec_position_label.grid(row=1, column=0)
        self.count_spec_position = ttk.Spinbox(self.count_spec_position_frame,
                                               from_=self.MIN_NUMBER_POSITION,
                                               to=self.MAX_NUMBER_POSITION,
                                               validate='all',
                                               validatecommand=(self.register(self._integer_filter), '%P', '%d'))
        self.count_spec_position.bind('<<Increment>>', self._on_increment)
        self.count_spec_position.bind('<<Decrement>>', self._on_decrement)
        self.count_spec_position.bind('<Return>', self._generate_spec_row)
        self.count_spec_position.set(1)
        self.count_spec_position.grid(row=1, column=1)

        self.main_spec_frame = tk.Frame(self)
        self.main_spec_frame.grid(pady=5, padx=5)
        self.column_number = tk.Label(self.main_spec_frame, text='№')
        self.column_number.grid(row=1, column=0)
        self.column_product = tk.Label(self.main_spec_frame, text='Назва товару')
        self.column_product.grid(row=1, column=1)
        self.measurement = tk.Label(self.main_spec_frame, text='Один. вим.')
        self.measurement.grid(row=1, column=2)
        self.quantity = tk.Label(self.main_spec_frame, text='К-сть')
        self.quantity.grid(row=1, column=3)
        self.price = tk.Label(self.main_spec_frame, text='Ціна')
        self.price.grid(row=1, column=4)
        self.sum = tk.Label(self.main_spec_frame, text='Сума')
        self.sum.grid(row=1, column=5)

        self._on_increment()

        self.button_frame = tk.Frame(self)
        self.button_frame.grid(sticky="ew")
        # self.save_spec_btn = tk.Button(self.button_frame, text='Експорт специфікації')
        # self.save_spec_btn.pack(side=tk.RIGHT, padx=5)

    def _integer_filter(self, inStr, acttyp):
        if acttyp == '1':  # insert
            if not inStr.isdigit():
                return False
            if int(inStr) < self.MIN_NUMBER_POSITION:
                self.count_spec_position.insert(0, self.MIN_NUMBER_POSITION)
                return False
            if int(inStr) > self.MAX_NUMBER_POSITION:
                return False
        return True

    def set_spec_values(self, data):
        num_of_rows = int(len(data) / 6)
        self.count_spec_position.set(num_of_rows)
        for entry in self.entries[::-1]:
            entry.destroy()
            self.entries.pop()
        for row in range(num_of_rows):
            self._on_increment()

        for entry, entry_data in zip(self.entries, data):
            entry.delete(0, tk.END)
            entry.insert(0, entry_data)

    def get_spec_value(self, event=None):
        """
        Pack row entry values in dictionary
        :return: list of row dictionary : list
        [{'num': '1', 'product': '...', 'measurement': '...', 'quantity': '...', 'price': '...', 'sum': '...'},
        {'num': '2', 'product': '...', 'measurement': '...', 'quantity': '...', 'price': '...', 'sum': '...'}]
        """
        respond = []
        row = {}
        i = 0
        for value in self.entries:
            i = i + 1
            if i == 1:
                row.setdefault('num', value.get())
            elif i == 2:
                row.setdefault('product', value.get())
            elif i == 3:
                row.setdefault('measurement', value.get())
            elif i == 4:
                row.setdefault('quantity', value.get())
            elif i == 5:
                row.setdefault('price', price_from_str(value.get()))
            elif i == 6:
                row.setdefault('sum', price_from_str(value.get()))
                respond.append(row)
                row = {}
                i = 0
        return respond

    def _on_increment(self, event=None):
        i = 0  # Entry position in frame grid
        if len(self.entries) < 180:  # limit in 30 rows
            if len(self.entries) >= 12:  # for third and more row
                i = int(self.entries[-6].get()) + 1
            elif len(self.entries) == 6:  # for second row
                i = 2
            elif not len(self.entries):
                i = 1
            self.en = ttk.Entry(self.main_spec_frame, width=2, takefocus=0)
            self.en.grid(row=i + 1, column=0)
            self.en.insert(0, i)
            self.en2 = ttk.Entry(self.main_spec_frame, width=50)
            self.en2.grid(row=i + 1, column=1)
            self.en3 = AutocompleteEntryWords(self.main_spec_frame, completevalues=self.measurement_autocomplete,
                                              width=10)
            self.en3.bind("<FocusOut>", self._add_measurement_autocomplete_list)
            self.en3.bind()
            self.en3.grid(row=i + 1, column=2)
            self.en4 = ttk.Entry(self.main_spec_frame, width=5)
            self.en4.bind("<FocusOut>", lambda event, row_num=i: self._calculate_price(row_num, event))
            self.en4.grid(row=i + 1, column=3)
            self.en5 = ttk.Entry(self.main_spec_frame, width=7)
            self.en5.bind("<FocusOut>", lambda event, row_num=i: self._calculate_price(row_num, event))
            self.en5.grid(row=i + 1, column=4)
            self.en6 = ttk.Entry(self.main_spec_frame, width=7)
            self.en6.grid(row=i + 1, column=5)
            self.entries.append(self.en)
            self.entries.append(self.en2)
            self.entries.append(self.en3)
            self.entries.append(self.en4)
            self.entries.append(self.en5)
            self.entries.append(self.en6)
        self.focus()  # remove focus from spinbox

    def _add_measurement_autocomplete_list(self, event=None):
        for entry in self.entries[2::6]:
            measurement_value = entry.get()
            if measurement_value and measurement_value not in self.measurement_autocomplete:
                self.measurement_autocomplete.append(measurement_value)
            entry.configure(completevalues=self.measurement_autocomplete)

    def _on_decrement(self, event=None):
        if len(self.entries) > 6:
            delete_list = self.entries[-1:-7:-1]  # delete row (last 6 Entry)
            for entry in delete_list:
                entry.destroy()
                self.entries.pop()
        self.focus()  # remove focus from spinbox

    def _generate_spec_row(self, event=None):
        new_row_count = int(self.count_spec_position.get())
        current_row_count = int(len(self.entries) / 6)
        delta = new_row_count - current_row_count

        if delta > 0:
            for i in range(delta):
                self._on_increment()
        elif delta < 0:
            for i in range(abs(delta)):
                self._on_decrement()

    def _calculate_price(self, row_num: int, event):
        quantity = self.entries[(row_num * 6) - 3].get()
        price = self.entries[(row_num * 6) - 2].get()
        if quantity and price:
            try:
                total_price = Decimal(price.replace(',', '.')) * Decimal(quantity.replace(',', '.'))
                round_total_price = total_price.quantize(Decimal("1.00"), ROUND_HALF_UP)
                self.entries[(row_num * 6) - 1].delete(0, tk.END)
                self.entries[(row_num * 6) - 1].insert(0, round_total_price)
            except decimal.InvalidOperation:
                print("Invalid price")
