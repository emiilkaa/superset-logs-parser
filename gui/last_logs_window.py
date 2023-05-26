import tkinter as tk
from datetime import datetime
from functools import partial
from tkinter import messagebox

from pandastable import addButton, Table

from gui.utils.save_utils import save_dataframe
from gui.utils.validate import digit_validation
from repository.log_repository import get_last_n_logs


def run(num_entry, parent):
    n = num_entry.get()
    if n:
        try:
            logs = get_last_n_logs(int(n))
        except Exception as e:
            messagebox.showerror('DB error', str(e), parent=parent)
            return
        table_root = tk.Toplevel(parent)
        table_root.title('Last {n} logs')
        table_root.geometry('1000x750')

        toolbar = tk.Frame(table_root)
        toolbar.pack()
        addButton(toolbar, 'Save results',
                  partial(save_dataframe, logs, f'logs_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv', table_root),
                  side='right')

        frame = tk.Frame(table_root)
        frame.pack(fill='both', expand=True)

        pt = Table(frame, dataframe=logs)
        pt.show()
    else:
        messagebox.showerror('Invalid request', 'Please enter all required parameters.', parent=parent)


def open_last_logs_window(master):
    root = tk.Toplevel(master)
    root.title('Get log by ID')
    root.geometry('650x150')

    id_frame = tk.Frame(root)
    id_frame.pack(side=tk.TOP, padx=10, pady=10)

    id_label = tk.Label(id_frame, text='How many logs you want to receive: ')
    id_label.pack(side=tk.LEFT)
    num_entry = tk.Entry(id_frame, validate='key', vcmd=(root.register(partial(digit_validation, root)), '%S'))
    num_entry.pack(side=tk.LEFT)

    button_frame = tk.Frame(root)
    button_frame.pack(side=tk.TOP, padx=10, pady=10)

    load_button = tk.Button(button_frame, text='Load', command=partial(run, num_entry, root))

    load_button.pack(side=tk.LEFT)

    return root
