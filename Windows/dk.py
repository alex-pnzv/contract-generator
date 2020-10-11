import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb

from Windows.directory import Directory
from Windows.dk_add import DkAdd
from Windows.dk_edit import EditDk


class Dk(Directory):
    def __init__(self,root,db):
        super().__init__()
        self.init_dk()
        self.db = db
        self.root = root
        self._search()
        self.init()
        self.minsize(600,300)
        self.protocol('WM_DELETE_WINDOW', self.update_dk_autocomplete)

    def init_dk(self):
        self.title('Єдиний закупівельний словник')
        self.geometry("700x400")
        self.focus_set()
        self.grab_set()

        self.tree = ttk.Treeview(self,column=("id","code","desc"), height=15, show="headings")
        self.tree.column('id', stretch=tk.NO, minwidth=0, width=0)
        self.tree.column('code',width=80, anchor=tk.W)
        self.tree.column('desc',width = 650, anchor=tk.W)
        self.tree.heading('code', text="Код")
        self.tree.heading('desc', text="Опис")
        self.tree.pack(fill='both',expand=True)
        self.tree.bind('<Double-1>',self.update_dk)

        vsb = ttk.Scrollbar(self.tree, orient="vertical", command=self.tree.yview)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.configure(yscrollcommand=vsb.set)

        self.popup_menu = tk.Menu(self, tearoff=0)
        self.popup_menu.add_command(label="Редагувати", command=self.update_dk)
        self.popup_menu.add_command(label="Видалити", command=self.delete_dk)

        self.add_button.configure(command=self.open_add_dk)
        self.edit_button.configure(command=self.update_dk)
        self.remove_button.configure(command=self.delete_dk)
        self.search_entry.bind('<KeyRelease>', self._search)


    def update_dk(self,event=None):
        if len(self.tree.selection()) == 1:
            selected_item = self.tree.selection()[0]
            dk_id = self.tree.set(selected_item,'#1')
            EditDk(self.db,dk_id,self._search)
            self.popup_menu.grab_release()

    def delete_dk(self):
        if len(self.tree.selection()) == 1:
            selected_item = self.tree.selection()[0]
            dk_id = self.tree.set(selected_item,"#1")
            result = mb.askyesno("Підтвердіть видалення", 'Ви впевнені що хочете видалити запис?')
            if result:
                self.db.del_dk(dk_id)
                self.tree.delete(selected_item)

    def open_add_dk(self):
        DkAdd(self.db,self._search)

    def _search(self, event=None):
        value = self.search_entry.get()
        rows = self.db.search_dk(value)
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', tk.END, values=row) for row in rows]
        if len(self.tree.get_children()) >= 1:
            child_id = self.tree.get_children()[0]
            self.tree.focus(child_id)
            self.tree.selection_set(child_id)


    def init(self):
        """initialise dialog"""
        # Button-3 is right click on windows
        self.tree.bind("<Button-3>", self.popup)

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

    def update_dk_autocomplete(self):
        self.root.dk_frame.update_autocomplete_dk_list()
        self.destroy()