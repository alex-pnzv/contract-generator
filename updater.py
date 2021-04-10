import threading
import zipfile
import tkinter as tk
from tkinter import ttk
import os

import requests
from win32api import GetFileVersionInfo, LOWORD, HIWORD
from packaging import version


class Main(tk.Tk):
    VERSION_URL = 'https://contract-generator-f02ca-default-rtdb.firebaseio.com/.json'
    UPDATE_URL = 'https://firebasestorage.googleapis.com/v0/b/contract-generator-f02ca.appspot.com/o/update.zip?alt=media'

    def __init__(self):
        super().__init__()
        self.title('Оновлення програми')
        self.minsize(300, 95)
        self.maxsize(300, 95)
        self.installed_version = ''
        self.latest_version = ''
        self.init_main()
        threading.Thread(target=self.set_current_version).start()

    def init_main(self):
        main_frame = tk.Frame(self)
        main_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        installed_version_frame = tk.Frame(main_frame)
        installed_version_frame.pack(fill=tk.X, padx=5)
        installed_version_label = tk.Label(installed_version_frame, text="Встановлена версія:", width=17, anchor=tk.W)
        installed_version_label.pack(side=tk.LEFT)
        self.installed_version_value = tk.Label(installed_version_frame, text=self.installed_version, width=10,
                                                anchor=tk.W)
        self.installed_version_value.pack(side=tk.LEFT)

        latest_version_frame = tk.Frame(main_frame)
        latest_version_frame.pack(fill=tk.X, padx=5)
        latest_version_label = tk.Label(latest_version_frame, text="Доступна версія:", width=17, anchor=tk.W)
        latest_version_label.pack(side=tk.LEFT, anchor='nw')
        self.latest_version_value = tk.Label(latest_version_frame, text=self.latest_version, width=10, anchor=tk.W)
        self.latest_version_value.pack(side=tk.LEFT, anchor='nw')

        update_btn_frame = tk.Frame(main_frame)
        update_btn_frame.pack(fill=tk.X, padx=5)
        self.progressBar = ttk.Progressbar(update_btn_frame, orient="horizontal", mode="determinate")
        self.update_btn = tk.Button(update_btn_frame, text="Оновити", command=self.update)

        self.statusbar = tk.Label(main_frame, text="", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X)

    def get_current_version(self):
        try:
            info = GetFileVersionInfo("main.exe", "\\")
            ms = info['FileVersionMS']
            ls = info['FileVersionLS']
            file_version = HIWORD(ms), LOWORD(ms), HIWORD(ls), LOWORD(ls)
            return ".".join([str(i) for i in file_version])
        except:
            return '0.0.0.0'

    def get_latest_version(self):
        last_version = requests.get(self.VERSION_URL).json()
        return str(last_version['latest_version'])

    def set_current_version(self):
        self.installed_version = self.get_current_version()
        self.installed_version_value.config(text=self.installed_version)

        self.latest_version = self.get_latest_version()
        self.latest_version_value.config(text=self.latest_version)
        if self.latest_version > self.installed_version:
            self.statusbar.config(text='Доступна нова версія програми.')
            self.update_btn.pack(side=tk.RIGHT)
        else:
            self.statusbar.config(text='У Вас встановлена остання версія програми')

    def update(self):
        if version.parse(self.installed_version) < version.parse(self.latest_version):
            threading.Thread(target=self.download_update).start()

    def download_update(self):
        self.update_btn.forget()
        self.progressBar.pack(fill=tk.X, side=tk.LEFT, expand=True)

        r = requests.get(self.UPDATE_URL, stream=True)
        file_size = int(r.headers['Content-Length'])
        num_bars = int(file_size / 1024)
        self.progressBar['value'] = 0
        self.progressBar['maximum'] = num_bars
        self.statusbar.config(text='Завантаження оновлення')
        with open('./update.zip', 'wb') as fp:
            for chunk in r.iter_content(1024):
                if chunk:
                    fp.write(chunk)
                    self.progressBar['value'] += 1

        self.statusbar.config(text='Установка оновлення')
        self.unzip()
        os.remove('update.zip')
        self.progressBar.forget()
        self.set_current_version()

    def unzip(self):
        with zipfile.ZipFile('update.zip') as zf:
            zf.extractall()


if __name__ == '__main__':
    app = Main()
    app.mainloop()
