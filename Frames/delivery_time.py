import tkinter as tk
import tkinter.ttk as ttk


class DeliveryTimeFrame():
    def __init__(self,root):
        self.delivery_time_main_frame = tk.Frame(root)
        self.delivery_time_main_frame.pack(fill=tk.X,padx=5,pady=5)
        delivery_time_label = tk.Label(self.delivery_time_main_frame, text="Срок поставки", width=14, anchor=tk.W)
        #cal = DateEntry(delivery_time, width=12,date_pattern='dd.mm.y', borderwidth=2)
        #cal.pack(padx=10, pady=10)

        delivery_time_label.pack(side=tk.LEFT, padx=5,pady=2)
        self.delivery_time = ttk.Entry(self.delivery_time_main_frame, validate='focusout')

        self.delivery_time.pack(side=tk.LEFT, fill=tk.X,  padx=7,pady=2,expand=True)

        self.error_photo = tk.PhotoImage(file='icons/warning2.png')
        self.error_label = tk.Label(self.delivery_time_main_frame, image=self.error_photo)
        #self.error_label.pack(side=tk.LEFT)

    def check_value(self,text:str):

        if len(text.split(',')) == 3:
            date = text.split(',')
            if int(date[1]) > 12:
                self.delivery_time.pack(side=tk.LEFT, fill=tk.X, padx=(7,0), pady=2, expand=True)
                self.error_label.pack(side=tk.RIGHT)
                return False
            self.error_label.pack_forget()
            self.delivery_time.pack(side=tk.LEFT, fill=tk.X, padx=7, pady=2, expand=True)
            return True
        elif len(text.split('.')) == 3:
            date = text.split('.')
            if int(date[1]) > 12:
                self.delivery_time.pack(side=tk.LEFT, fill=tk.X, padx=(7, 0), pady=2, expand=True)
                self.error_label.pack(side=tk.RIGHT)
                return False
            self.delivery_time.pack(side=tk.LEFT, fill=tk.X, padx=7, pady=2, expand=True)
            self.error_label.pack_forget()
            return True
        else:
            self.delivery_time.pack(side=tk.LEFT, fill=tk.X, padx=(7, 0), pady=2, expand=True)
            self.error_label.pack(side=tk.RIGHT)
            return False