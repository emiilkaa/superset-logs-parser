import datetime
import tkinter as tk
from functools import partial

from pandastable import Table, addButton

from gui.utils.save_utils import save_dataframe
from repository.log_repository import get_all_logs


def open_all_logs_window(master):
    logs = get_all_logs()

    root = tk.Toplevel(master)
    root.title('All the logs')
    root.geometry('1000x750')

    toolbar = tk.Frame(root)
    toolbar.pack()
    addButton(toolbar, 'Save results', partial(save_dataframe, logs, f'logs_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.csv', root), side='right')

    frame = tk.Frame(root)
    frame.pack(fill='both', expand=True)

    pt = Table(frame, dataframe=logs)
    pt.show()
