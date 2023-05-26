import datetime
import tkinter as tk
from functools import partial

from pandastable import Table, addButton

from gui.utils.save_utils import save_dataframe
from repository.log_repository import count_users_using_each_dashboard


def open_count_users_window(master):
    logs = count_users_using_each_dashboard()

    root = tk.Toplevel(master)
    root.title('Count of users using each dashboard')
    root.geometry('1000x750')

    toolbar = tk.Frame(root)
    toolbar.pack()
    addButton(toolbar, 'Save results', partial(save_dataframe, logs, f'count_of_users_using_dashboards_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.csv', root), side='right')

    frame = tk.Frame(root)
    frame.pack(fill='both', expand=True)

    pt = Table(frame, dataframe=logs)
    pt.show()
