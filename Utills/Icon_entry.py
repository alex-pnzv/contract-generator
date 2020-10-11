import tkinter as tk
import tkinter.ttk as ttk

class SearchEntry(ttk.Widget):
    """
    Customized version of a ttk Entry widget with an element included in the
    text field. Custom elements can be created using either the vsapi engine
    to obtain system theme provided elements (like the pin used here) or by using
    the "image" element engine to create an element using Tk images.

    Note: this class needs to be registered with the Tk interpreter before it gets
    used by calling the "register" static method.
    """
    def __init__(self, master, **kw):
        kw["style"] = "Search.Entry"
        ttk.Widget.__init__(self, master, 'ttk::entry', kw)
    def get(self):
        return self.tk.call(self._w, 'get')
    def set(self, value):
        self.tk.call(self._w, 'set', value)
    @staticmethod
    def register(root):
        style = ttk.Style()
        # There seems to be some argument parsing bug in tkinter.ttk so cheat and eval
        # the raw Tcl code to add the vsapi element for a pin.
        ##root.eval('''ttk::style element create pin vsapi EXPLORERBAR 3 {
        ##    {pressed !selected} 3
        ##    {active !selected} 2
        ##    {pressed selected} 6
        ##    {active selected} 5
        ##    {selected} 4
        ##    {} 1
        ##}''')
        add_button_pic = tk.PhotoImage('add',file='../Windows/add.png')
        style.element_create('pin','image','add')
        #style.element_create("pin", "vsapi", "EXPLORERBAR", "3", [(["selected"], 4),([], 1)])
        style.layout("Search.Entry", [
            ("Search.Entry.field", {'sticky': 'nswe', 'children': [
                ("Search.Entry.background", {'sticky':'nswe', 'children': [
                    ("Search.Entry.padding", {'sticky':'nswe', 'children': [
                        ("Search.Entry.textarea", {'sticky':'nswe'})
                    ]})
                ]}),
                ("Search.Entry.pin", {'sticky': 'e'})
            ]})
        ])
        style.configure("Search.Entry", padding=(1, 1, 14, 1))
        style.map("Search.Entry", **style.map("TEntry"))

if __name__ == '__main__':
    root = tk.Tk()
    text = tk.StringVar()
    SearchEntry.register(root)
    frame = ttk.Frame(root)
    text.set("some example text ...")
    e1 = ttk.Entry(frame, textvariable=text)
    e2 = SearchEntry(frame, textvariable=text)
    e1.grid(sticky="news", padx=2, pady=2)
    e2.grid(sticky="news", padx=2, pady=2)
    frame.grid(sticky = "news", padx=2, pady=2)
    root.grid_columnconfigure(0, weight = "1")
    root.grid_rowconfigure(0, weight = "1")
    root.mainloop()