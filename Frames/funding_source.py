import tkinter as tk
import tkinter.ttk as ttk

class FundingSourceFrame():
    def __init__(self,root):
        source_of_funding_frame = tk.Frame(root)
        source_of_funding_frame.pack(fill=tk.X,padx=5)
        source_of_funding_label = tk.Label(source_of_funding_frame, text='Фінансування',width=14, anchor=tk.W)
        source_of_funding_label.pack(side=tk.LEFT,padx=5)
        self.funding_value = tk.IntVar()

        source_of_funding1 = tk.Radiobutton(source_of_funding_frame,variable=self.funding_value, value=1,text='Кошти МБ',command=self.check)
        source_of_funding1.pack(side=tk.LEFT,fill=tk.X, padx=5)
        source_of_funding2 = tk.Radiobutton(source_of_funding_frame, variable=self.funding_value, value=2, text='Кошти СФ',command=self.check)
        source_of_funding2.pack(side=tk.LEFT, fill=tk.X, padx=5)
        source_of_funding3 = tk.Radiobutton(source_of_funding_frame, variable=self.funding_value, value=3, text='Інше', command=self.check)
        source_of_funding3.pack(side=tk.LEFT,padx=(5,0))

        self.source_of_funding_entry = ttk.Entry(source_of_funding_frame)
        self.funding_value.set(1)

    def check(self):
        if self.funding_value.get() == 3:
            self.source_of_funding_entry.pack(fill=tk.X,padx=(0,5))
        else:
            self.source_of_funding_entry.pack_forget()

    def get_funding_value(self):
        val = self.funding_value.get()
        if val == 1:
            return "кошти місцевого бюджету"
        elif val == 2:
            return 'кошти спеціального фонду'
        elif val == 3:
            return self.source_of_funding_entry.get()

    def set_funding_value(self,value):
        if value == 'кошти місцевого бюджету':
            self.funding_value.set(1)
        elif value == 'кошти спеціального фонду':
            self.funding_value.set(2)
        else:
            self.funding_value.set(3)
            self.source_of_funding_entry.delete(0,tk.END)
            self.source_of_funding_entry.insert(0,value)