import tkinter as tk
import tkinter.ttk as ttk

class ContractFrame():
    def __init__(self,root):
        contract_frame = tk.Frame(root)
        contract_frame.pack(fill=tk.X,padx=5)
        contract_label = tk.Label(contract_frame, text="Предмет договору", width=14, anchor=tk.W)
        contract_label.pack(side=tk.LEFT, padx=5,pady=(5,0))
        self.contract = ttk.Entry(contract_frame)
        self.contract.pack(fill=tk.X, padx=7,pady=(5,0))