import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as mb

from Windows.address_add import AddAddress
from Windows.address_edit import EditAddress
from Windows.directory import Directory

class Address(Directory):
    def __init__(self,root,db):
        self.root = root
        super().__init__()
        self.title('Адреси поставки')
        self.minsize(700,300)
        self.init_users()
        self.db = db
        self._search()
        self.protocol('WM_DELETE_WINDOW', self.update_address_autocomplete)

    def init_users(self):
        self.tree = ttk.Treeview(self,column=('id','name','address' ), height=15, show="headings")
        self.tree.column('id',stretch=tk.NO, minwidth=0, width=0)
        self.tree.column('name', width=250, anchor=tk.W)
        self.tree.column('address', width=450, anchor=tk.W)
        self.tree.heading('name', text="Назва закладу")
        self.tree.heading('address', text="Адреса")
        self.tree.bind("<Double-1>", self.update_address)
        self.tree.bind("<Button-3>", self.popup)
        self.tree.pack(fill='both',expand=True)

        vsb = ttk.Scrollbar(self.tree, orient="vertical", command=self.tree.yview)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.configure(yscrollcommand=vsb.set)

        self.popup_menu = tk.Menu(self, tearoff=0)
        self.popup_menu.add_command(label="Редагувати", command=self.update_address)
        self.popup_menu.add_command(label="Видалити", command=self.delete_address)

        self.add_button.configure(command=self.open_add_addres)
        self.edit_button.configure(command=self.update_address)
        self.remove_button.configure(command=self.delete_address)
        self.search_entry.bind('<KeyRelease>', self._search)

    def open_add_addres(self):
        AddAddress(self.db,self._search)

    def update_address(self, event=None):
        selected_item = self.tree.selection()[0]
        user_id = self.tree.set(selected_item,"#1")
        EditAddress(self.root,self.db,user_id,self._search)
        self.focus_get()
        self.grab_release()

    def delete_address(self):
        if len(self.tree.selection()) == 1:
            selected_item = self.tree.selection()[0]
            address_id = self.tree.set(selected_item,"#1")
            result = mb.askyesno("Підтвердіть видалення", 'Ви впевнені що хочете видалити запис?')
            if result:
                self.db.del_address(address_id)
                self.tree.delete(selected_item)

    def _search(self, event=None):
        value = self.search_entry.get()
        rows = self.db.search_address(value)
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', tk.END, values=row) for row in rows]
        if len(self.tree.get_children()) >= 1:
            child_id = self.tree.get_children()[0]
            self.tree.focus(child_id)
            self.tree.selection_set(child_id)

    def popup(self, event):
        """action in event of button 3 on tree view"""
        # select row under mouse
        iid = self.tree.identify_row(event.y)
        if iid:
            # mouse pointer over item
            self.tree.selection_set(iid)
            self.popup_menu.post(event.x_root, event.y_root)
        else:
            # mouse pointer not over item
            # occurs when items do not fill frame
            # no action required
            pass

    def update_address_autocomplete(self):
        self.root.delivery_address_frame.update_autocomplete_address_list()
        self.destroy()
