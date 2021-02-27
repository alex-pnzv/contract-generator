import tkinter as tk
import tkinter.ttk as ttk


class MultipleAutocompleteEntry(ttk.Entry):
    """
    Subclass of :class:`ttk.Entry` that features autocompletion.

    To enable autocompletion use :meth:`set_completion_list` to define
    a list of possible strings to hit.
    To cycle through hits use down and up arrow keys.
    """

    def __init__(self, master=None, completevalues=None, **kwargs):
        """
        Create an AutocompleteEntry.

        :param master: master widget
        :type master: widget
        :param completevalues: autocompletion values
        :type completevalues: list
        :param kwargs: keyword arguments passed to the :class:`ttk.Entry` initializer
        """
        ttk.Entry.__init__(self, master, **kwargs)
        self._completion_list = completevalues
        self.set_completion_list(completevalues)
        self.position = 0

    def set_completion_list(self, completion_list):
        """
        Set a new auto completion list

        :param completion_list: completion values
        :type completion_list: list
        """
        self._completion_list = sorted(completion_list, key=str.lower)  # Work with a sorted list
        self.position = 0
        self.bind('<KeyRelease>', self.handle_keyrelease)

    def autocomplete(self, delta=0):
        """
        Autocomplete the Entry.

        :param delta: 0, 1 or -1: how to cycle through possible hits
        :type delta: int
        """
        self.position = len(self.get())
        entry_value = self.get()
        separator_index = [i for i in range(len(entry_value)) if entry_value.startswith(',', i)]
        for element in self._completion_list:
            if separator_index:
                last_value = self.get()[separator_index[-1]+1:]
                if str(element).lower().startswith(str(last_value.strip()).lower()):
                    if last_value.startswith(' '):
                        self.delete(separator_index[-1] + 1, tk.END)
                        self.insert(separator_index[-1] + 1, ' ')
                        self.insert(separator_index[-1] + 2, element)
                        self.select_range(self.position, tk.END)
                    else:
                        self.delete(separator_index[-1] + 1, tk.END)
                        self.insert(separator_index[-1] + 1, element)
                        self.select_range(self.position, tk.END)
            else:
                if str(element).lower().startswith(str(self.get()).lower()):
                    self.delete(0, tk.END)
                    self.insert(0, element)
                    self.select_range(self.position, tk.END)
                    break

    def handle_keyrelease(self, event):
        """
        Event handler for the keyrelease event on this widget.

        :param event: Tkinter event
        """
        if event.keysym == "Return":
            self.handle_return(None)
            return
        if len(event.keysym) == 1 or len(event.keysym) == 2:
            self.autocomplete()

    def handle_return(self, event):
        """
        Function to bind to the Enter/Return key so if Enter is pressed the selection is cleared.

        :param event: Tkinter event
        """
        self.icursor(tk.END)
        self.selection_clear()

    def config(self, **kwargs):
        """Alias for configure"""
        self.configure(**kwargs)

    def configure(self, **kwargs):
        """Configure widget specific keyword arguments in addition to :class:`ttk.Entry` keyword arguments."""
        if "completevalues" in kwargs:
            self.set_completion_list(kwargs.pop("completevalues"))
        return ttk.Entry.configure(self, **kwargs)

    def cget(self, key):
        """Return value for widget specific keyword arguments"""
        if key == "completevalues":
            return self._completion_list
        return ttk.Entry.cget(self, key)

    def keys(self):
        """Return a list of all resource names of this widget."""
        keys = ttk.Entry.keys(self)
        keys.append("completevalues")
        return keys

    def __setitem__(self, key, value):
        self.configure(**{key: value})

    def __getitem__(self, item):
        return self.cget(item)
