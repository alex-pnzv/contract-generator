import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as mb


class Templates(tk.Toplevel):
    def __init__(self, db, getid, **kw):
        super().__init__(**kw)
        self.db = db
        self.get_id = getid
        self.title("Шаблони")
        self.minsize(250, 200)
        self.focus_set()
        self.grab_set()
        self.init_frame()
        self._insert_value()

    def init_frame(self):
        self.template_tree = ttk.Treeview(self, column=('id', 'name'), height=14, show="headings")
        self.template_tree.column('id', width=0, minwidth=0, stretch=tk.NO)
        self.template_tree.column('name')
        self.template_tree.heading('name', text='Назва шаблону')
        self.template_tree.pack(fill=tk.BOTH, expand=True)
        self.template_tree.bind('<Double-1>', self._select_id)
        self.template_tree.bind("<Button-3>", self.popup)

        vsb = ttk.Scrollbar(self.template_tree, orient="vertical", command=self.template_tree.yview)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)

        self.template_tree.configure(yscrollcommand=vsb.set)

        self.popup_menu = tk.Menu(self, tearoff=0)
        self.popup_menu.add_command(label="Вибрати", command=self._select_id)
        self.popup_menu.add_command(label="Видалити", command=self._del_selected_template)

    def _insert_value(self):
        rows = self.db.get_templates()
        [self.template_tree.insert('', tk.END, values=row) for row in rows]
        if len(self.template_tree.get_children()) >= 1:
            child_id = self.template_tree.get_children()[0]
            self.template_tree.focus(child_id)
            self.template_tree.selection_set(child_id)

    def _select_id(self, event=None):
        items = self.template_tree.selection()[0]
        template_id = self.template_tree.set(items, "#1")
        self.get_id(template_id)
        self.destroy()

    def _del_selected_template(self):
        item = self.template_tree.selection()[0]
        template_id = self.template_tree.set(item, "#1")
        result = mb.askyesno("Підтвердіть видалення", 'Ви впевнені, що хочете видалити шаблон?')
        if result:
            self.template_tree.delete(item)
            self.db.del_template_by_id(template_id)

    def popup(self, event):
        iid = self.template_tree.identify_row(event.y)
        if iid:
            self.template_tree.selection_set(iid)
            self.popup_menu.post(event.x_root, event.y_root)
        else:
            return
