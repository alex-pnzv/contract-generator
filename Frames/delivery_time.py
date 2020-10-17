import tkinter as tk
import tkinter.ttk as ttk
from icons import icons


class DeliveryTimeFrame:
    def __init__(self,root):
        self.delivery_time_main_frame = tk.Frame(root)
        self.delivery_time_main_frame.pack(fill=tk.X,padx=5,pady=5)
        delivery_time_label = tk.Label(self.delivery_time_main_frame, text="Срок поставки", width=14, anchor=tk.W)

        delivery_time_label.pack(side=tk.LEFT, padx=5,pady=2)
        self.delivery_time = ttk.Entry(self.delivery_time_main_frame, validate='focusout')

        self.delivery_time.pack(side=tk.LEFT, fill=tk.X,  padx=7,pady=2,expand=True)

        self.error_photo = tk.PhotoImage(data=icons.warning)
        self.error_label = tk.Label(self.delivery_time_main_frame, image=self.error_photo)

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