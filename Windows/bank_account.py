import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as mb
from Windows.bank_account_add import AddBankAccount
from Windows.bank_account_edit import EditBankAccount
from Windows.directory import Directory


class BankAccount(Directory):
    def __init__(self, root, db, **kw):
        super().__init__(**kw)
        self.title('Банківські рахунки')
        self.db = db
        self.root = root
        self.grab_set()
        self.focus_set()
        self.init_main_frame()
        self.get_all_bank_accounts()
        self.minsize(400, 350)
        self.protocol('WM_DELETE_WINDOW', self.update_bank_account_autocomplete)

    def init_main_frame(self):
        self.buttons_frame = tk.Frame(self)
        self.buttons_frame.pack(side=tk.TOP, fill=tk.X)

        self.bank_account_tree = ttk.Treeview(self, column=('id', "name", 'value'), height=15, show='headings')
        self.bank_account_tree.column('id', stretch=tk.NO, minwidth=0, width=0)
        self.bank_account_tree.column('name', width=150, anchor=tk.W)
        self.bank_account_tree.column('value', width=200, anchor=tk.W)
        self.bank_account_tree.heading('name', text="Назва")
        self.bank_account_tree.heading('value', text="Рахунок")
        self.bank_account_tree.pack(fill=tk.BOTH, expand=True)
        self.bank_account_tree.bind("<Double-1>", self.update_bank_account)
        self.bank_account_tree.bind("<Button-3>", self.popup)

        vsb = ttk.Scrollbar(self.bank_account_tree, orient="vertical", command=self.bank_account_tree.yview)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)

        self.bank_account_tree.configure(yscrollcommand=vsb.set)

        self.popup_menu = tk.Menu(self, tearoff=0)
        self.popup_menu.add_command(label="Редагувати", command=self.update_bank_account)
        self.popup_menu.add_command(label="Видалити", command=self.delete_bank_account)

        self.add_button.configure(command=self.open_add_bank_account)
        self.edit_button.configure(command=self.update_bank_account)
        self.remove_button.configure(command=self.delete_bank_account)
        self.search_entry.bind('<KeyRelease>', self._search)

    def update_bank_account(self, event=None):
        selected_id = self.bank_account_tree.selection()[0]
        id = self.bank_account_tree.set(selected_id, "#1")
        EditBankAccount(self.db, id, self.get_all_bank_accounts)

    def delete_bank_account(self):
        if len(self.bank_account_tree.selection()) == 1:
            selected_item = self.bank_account_tree.selection()
            id = self.bank_account_tree.set(selected_item, '#1')
            result = mb.askyesno("Підтвердіть видалення", 'Ви впевнені що хочете видалити запис?')
            if result:
                self.bank_account_tree.delete(selected_item)
                self.db.del_bank_account(id)

    def open_add_bank_account(self):
        AddBankAccount(self.db, self.get_all_bank_accounts)

    def _search(self, event):
        value = self.search_entry.get()
        rows = self.db.search_bank_account(value)
        [self.bank_account_tree.delete(i) for i in self.bank_account_tree.get_children()]
        [self.bank_account_tree.insert('', tk.END, values=row) for row in rows]
        if len(self.bank_account_tree.get_children()) >= 1:
            child_id = self.bank_account_tree.get_children()[0]
            self.bank_account_tree.focus(child_id)
            self.bank_account_tree.selection_set(child_id)

    def get_all_bank_accounts(self):
        self.db.c.execute("SELECT * FROM bank_accounts ORDER BY name")
        [self.bank_account_tree.delete(i) for i in self.bank_account_tree.get_children()]
        [self.bank_account_tree.insert('', tk.END, values=row) for row in self.db.c.fetchall()]
        if len(self.bank_account_tree.get_children()) >= 1:
            child_id = self.bank_account_tree.get_children()[0]
            self.bank_account_tree.focus(child_id)
            self.bank_account_tree.selection_set(child_id)

    def popup(self, event):
        iid = self.bank_account_tree.identify_row(event.y)
        if iid:
            self.bank_account_tree.selection_set(iid)
            self.popup_menu.post(event.x_root, event.y_root)
        else:
            return

    def update_bank_account_autocomplete(self):
        self.root.bank_account_frame.update_autocomplete()
        self.destroy()
