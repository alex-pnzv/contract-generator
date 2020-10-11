import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as mb

from Windows.directory import Directory
from Windows.users_add import UserAdd
from Windows.users_edit import EditUsers


class Users(Directory):
    def __init__(self,root,db):
        self.root = root
        super().__init__()
        self.init_users()
        self.db = db
        self._search()
        self.protocol('WM_DELETE_WINDOW', self.update_users_autocomplete)

    def init_users(self):
        self.title('Контрагенти')
        self.minsize(400,250)
        self.focus_set()
        self.grab_set()

        self.tree = ttk.Treeview(self,column=('id','edrpou','name' ), height=15, show="headings")
        self.tree.column('id',stretch=tk.NO, minwidth=0, width=0)
        self.tree.column('edrpou', width=80, anchor=tk.W)
        self.tree.column('name', width=200, anchor=tk.W)
        self.tree.heading('name', text="ПІБ")
        self.tree.heading('edrpou', text="ЄДРПОУ")
        #self.tree.heading('iban', text="IBAN")
        #self.tree.heading('bank_mfo', text="МФО банку")
        #self.tree.heading('bank_name', text="Назва банку")
        #self.tree.heading('postal_code', text="Індекс")
        #self.tree.heading('region', text="Область")
        #self.tree.heading('district', text="Район")
        #self.tree.heading('city', text="Місто")
        #self.tree.heading('street', text="Вулиця")
        #self.tree.heading('house_num', text="будинок")
        #self.tree.heading('telephone', text="телефон")
        self.tree.bind("<Double-1>", self.update_user)
        self.tree.pack(fill="both",expand=True)
        self.tree.bind("<Button-3>", self.popup)

        scroll = ttk.Scrollbar(self.tree, orient='vertical', command=self.tree.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)

        self.popup_menu = tk.Menu(self, tearoff=0)
        self.popup_menu.add_command(label="Редагувати",command=self.update_user)
        self.popup_menu.add_command(label="Видалити", command=self.delete_user)

        self.add_button.configure(command=self.open_add_user)
        self.edit_button.configure(command=self.update_user)
        self.remove_button.configure(command=self.delete_user)
        self.search_entry.bind('<KeyRelease>', self._search)

    def open_add_user(self):
        UserAdd(self.db,self._search)

    def update_user(self,event=None):
        selected_item = self.tree.selection()[0]
        user_id = self.tree.set(selected_item,"#1")
        EditUsers(self.db,user_id,self._search)
        self.focus_get()
        self.grab_release()

    def delete_user(self):
        if len(self.tree.selection()) == 1:
            selected_item = self.tree.selection()[0]
            user_id = self.tree.set(selected_item,"#1")
            result = mb.askyesno("Підтвердіть видалення", 'Ви впевнені що хочете видалити запис?')
            if result:
                self.db.del_user(user_id)
                self.tree.delete(selected_item)

    def _search(self, event=None):
        value = self.search_entry.get()
        rows = self.db.search_user(value)
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

    def update_users_autocomplete(self):
        self.root.user_frame.update_autocomplete_edrpou_list()
        self.destroy()
