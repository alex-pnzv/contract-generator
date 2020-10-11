import tkinter as tk
import tkinter.ttk as ttk


class SumFrame():
    def __init__(self, root):
        sum_frame = tk.Frame(root)
        sum_frame.pack(fill=tk.X, padx=5)
        sum_label = tk.Label(sum_frame, text="Сума", width=14, anchor=tk.W)
        sum_label.pack(side=tk.LEFT, padx=5, pady=5)
        self.sum = ttk.Entry(sum_frame)
        self.sum.pack(fill=tk.X, padx=7, pady=5)
