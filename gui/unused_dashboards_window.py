import datetime
import tkinter as tk
from functools import partial
from tkinter import messagebox

from pandastable import addButton, Table

from gui.utils.save_utils import save_dataframe
from repository.log_repository import get_last_dashboards_usage

DATETIME_FORMAT = '%d.%m.%Y %H:%M:%S'


def run(start_entry, parent):
    start = start_entry.get()

    start_dttm = None
    try:
        if start:
            start_dttm = datetime.datetime.strptime(start, DATETIME_FORMAT)
    except ValueError:
        messagebox.showerror('Invalid format', 'Please enter date in format DD.MM.YYYY HH:mm:SS')
        return

    try:
        logs = get_last_dashboards_usage(start_dttm)
    except Exception as e:
        messagebox.showerror('DB error', str(e), parent=parent)
        return
    table_root = tk.Toplevel(parent)
    table_root.title('Last dashboards usage')
    table_root.geometry('1000x750')

    toolbar = tk.Frame(table_root)
    toolbar.pack()
    addButton(toolbar, 'Save results',
              partial(save_dataframe, logs,
                      f'last_dashboards_usage_{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}.csv',
                      table_root),
              side='right')

    frame = tk.Frame(table_root)
    frame.pack(fill='both', expand=True)

    pt = Table(frame, dataframe=logs)
    pt.show()


def open_unused_dashboards_window(master):
    root = tk.Toplevel(master)
    root.title('Count dashboards usage')

    current_time = datetime.datetime.now()

    start_time_label = tk.Label(root, text='Time no later than which dashboards were used: ')
    start_time_label.grid(row=0, column=0, padx=5, pady=5)
    start_time_entry = tk.Entry(root)
    start_time_entry.insert(tk.END, (current_time - datetime.timedelta(days=30)).strftime(DATETIME_FORMAT))
    start_time_entry.grid(row=0, column=1, padx=5, pady=5)

    note_label = tk.Label(root, text='Date field can be left blank if no filtering is required.', font=('Arial', 7))
    note_label.grid(row=1, column=1, padx=5, pady=5)

    load_button = tk.Button(root, text='Load', width=10, command=partial(run, start_time_entry, root))
    load_button.grid(row=2, column=1, padx=5, pady=5)

    return root
