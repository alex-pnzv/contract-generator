import tkinter as tk

class ContractType():
    def __init__(self,root,onchangecommand):
        contract_type_frame = tk.Frame(root)
        contract_type_frame.pack(fill=tk.X,padx=5)

        contract_type_label = tk.Label(contract_type_frame,text="Тип договору",width=14, anchor=tk.W)
        contract_type_label.pack(side=tk.LEFT,padx=5)

        self.contract_type_value = tk.StringVar()

        contract_type1 = tk.Radiobutton(contract_type_frame, variable=self.contract_type_value, value='product', text='Товар',command=onchangecommand)
        contract_type1.pack(side=tk.LEFT,padx=5)
        contract_type2 = tk.Radiobutton(contract_type_frame, variable=self.contract_type_value, value='service', text='Послуга',command=onchangecommand)
        contract_type2.pack(side=tk.LEFT,padx=5)

        self.contract_type_value.set("product")
