import datetime
import tkinter as tk
from functools import partial
from tkinter import messagebox

from pandastable import addButton, Table

from gui.utils.save_utils import save_dataframe
from gui.utils.validate import digit_validation
from repository.log_repository import get_user_actions


def run(user_id_entry, parent):
    user_id = user_id_entry.get()

    if user_id:
        try:
            logs = get_user_actions(int(user_id))
        except Exception as e:
            messagebox.showerror('DB error', str(e), parent=parent)
            return
        table_root = tk.Toplevel(parent)
        table_root.title(f'Logs by user with ID {user_id}')
        table_root.geometry('1000x750')

        toolbar = tk.Frame(table_root)
        toolbar.pack()
        addButton(toolbar, 'Save results',
                  partial(save_dataframe, logs,
                          f'logs_user_{user_id}_{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}.csv',
                          table_root),
                  side='right')

        frame = tk.Frame(table_root)
        frame.pack(fill='both', expand=True)

        pt = Table(frame, dataframe=logs)
        pt.show()
    else:
        messagebox.showerror('Invalid request', 'Please enter all required parameters.', parent=parent)


def open_user_logs_window(master):
    root = tk.Toplevel(master)
    root.title('Get logs by user')

    user_id_label = tk.Label(root, text='User ID: ')
    user_id_label.grid(row=0, column=1, padx=5, pady=5)
    user_id_entry = tk.Entry(root, validate='key', vcmd=(root.register(partial(digit_validation, root)), '%S'))
    user_id_entry.grid(row=0, column=2, padx=5, pady=5)

    load_button = tk.Button(root, text='Load', width=10, command=partial(run, user_id_entry, root))
    load_button.grid(row=4, column=2, padx=5, pady=5)

    return root
