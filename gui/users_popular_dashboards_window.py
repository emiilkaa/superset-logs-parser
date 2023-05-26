import datetime
import tkinter as tk
from functools import partial

from pandastable import Table, addButton

from gui.utils.save_utils import save_dataframe
from repository.log_repository import get_popular_dashboards_by_users


def open_users_popular_dashboards_window(master):
    logs = get_popular_dashboards_by_users()

    root = tk.Toplevel(master)
    root.title('Popular actions by each dashboard')
    root.geometry('1000x750')

    toolbar = tk.Frame(root)
    toolbar.pack()
    addButton(toolbar, 'Save results', partial(save_dataframe, logs,
                                               f'users_and_dashboards_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
                                               root), side='right')

    frame = tk.Frame(root)
    frame.pack(fill='both', expand=True)

    pt = Table(frame, dataframe=logs)
    pt.show()
