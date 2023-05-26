import datetime
import tkinter as tk
from functools import partial

from pandastable import Table, addButton

from gui.utils.save_utils import save_dataframe
from repository.log_repository import get_duration_stats_by_action


def open_duration_stats_window(master):
    logs = get_duration_stats_by_action()

    root = tk.Toplevel(master)
    root.title('Duration stats by actions')
    root.geometry('1000x750')

    toolbar = tk.Frame(root)
    toolbar.pack()
    addButton(toolbar, 'Save results',
              partial(save_dataframe, logs, f'duration_stats_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
                      root), side='right')

    frame = tk.Frame(root)
    frame.pack(fill='both', expand=True)

    pt = Table(frame, dataframe=logs)
    pt.show()
