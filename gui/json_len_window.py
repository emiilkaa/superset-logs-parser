import datetime
import tkinter as tk
from functools import partial

from pandastable import Table, addButton

from gui.utils.save_utils import save_dataframe
from repository.log_repository import json_len_by_dashboard


def open_json_len_window(master):
    logs = json_len_by_dashboard()

    root = tk.Toplevel(master)
    root.title('Average extra data size for each dashboard')
    root.geometry('1000x750')

    toolbar = tk.Frame(root)
    toolbar.pack()
    addButton(toolbar, 'Save results', partial(save_dataframe, logs,
                                               f'json_length_by_dashboard_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
                                               root), side='right')

    frame = tk.Frame(root)
    frame.pack(fill='both', expand=True)

    pt = Table(frame, dataframe=logs)
    pt.show()
