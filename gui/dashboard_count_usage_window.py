import datetime
import tkinter as tk
from functools import partial
from tkinter import messagebox

from pandastable import addButton, Table

from gui.utils.save_utils import save_dataframe
from repository.log_repository import count_dashboards_usage

DATETIME_FORMAT = '%d.%m.%Y %H:%M:%S'

TIME_DELTAS = [
    datetime.timedelta(minutes=30),
    datetime.timedelta(hours=1),
    datetime.timedelta(days=1),
    datetime.timedelta(weeks=1),
    datetime.timedelta(days=30)
]


def set_time(time_id, start_time_entry, end_time_entry):
    current_time = datetime.datetime.now()

    start = current_time - TIME_DELTAS[time_id]

    start_time_entry.delete(0, 'end')
    start_time_entry.insert(tk.END, start.strftime(DATETIME_FORMAT))
    end_time_entry.delete(0, 'end')
    end_time_entry.insert(tk.END, current_time.strftime(DATETIME_FORMAT))


def run(start_entry, end_entry, parent):
    start = start_entry.get()
    end = end_entry.get()

    start_dttm = None
    end_dttm = None
    try:
        if start:
            start_dttm = datetime.datetime.strptime(start, DATETIME_FORMAT)
        if end:
            end_dttm = datetime.datetime.strptime(end, DATETIME_FORMAT)
    except ValueError:
        messagebox.showerror('Invalid format', 'Please enter dates in format DD.MM.YYYY HH:mm:SS')
        return

    try:
        logs = count_dashboards_usage(start_dttm, end_dttm)
    except Exception as e:
        messagebox.showerror('DB error', str(e), parent=parent)
        return
    table_root = tk.Toplevel(parent)
    title = 'Dashboards usage'
    if start_dttm is not None:
        title += f' from {start}'
    if end_dttm is not None:
        title += f' to {end}'
    table_root.title(title)
    table_root.geometry('1000x750')

    toolbar = tk.Frame(table_root)
    toolbar.pack()
    addButton(toolbar, 'Save results',
              partial(save_dataframe, logs,
                      f'dashboards_usage_{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}.csv',
                      table_root),
              side='right')

    frame = tk.Frame(table_root)
    frame.pack(fill='both', expand=True)

    pt = Table(frame, dataframe=logs)
    pt.show()


def open_dashboard_count_usage_window(master):
    root = tk.Toplevel(master)
    root.title('Count dashboards usage')

    current_time = datetime.datetime.now()

    start_time_label = tk.Label(root, text='Start time: ')
    start_time_label.grid(row=0, column=1, padx=5, pady=5)
    start_time_entry = tk.Entry(root)
    start_time_entry.insert(tk.END, (current_time - datetime.timedelta(days=1)).strftime(DATETIME_FORMAT))
    start_time_entry.grid(row=0, column=2, padx=5, pady=5)

    end_time_label = tk.Label(root, text='End time: ')
    end_time_label.grid(row=1, column=1, padx=5, pady=5)
    end_time_entry = tk.Entry(root)
    end_time_entry.insert(tk.END, current_time.strftime(DATETIME_FORMAT))
    end_time_entry.grid(row=1, column=2, padx=5, pady=5)

    note_label = tk.Label(root, text='Date fields can be left blank if no filtering is required.', font=('Arial', 7))
    note_label.grid(row=3, column=2, padx=5, pady=5)

    text1_button = tk.Button(root, text='Last 30 minutes',
                             command=partial(set_time, 0, start_time_entry, end_time_entry))
    text1_button.grid(row=0, column=0, padx=2, pady=5)

    text2_button = tk.Button(root, text='Last hour', command=partial(set_time, 1, start_time_entry, end_time_entry))
    text2_button.grid(row=1, column=0, padx=2, pady=5)

    text3_button = tk.Button(root, text='Last day', command=partial(set_time, 2, start_time_entry, end_time_entry))
    text3_button.grid(row=2, column=0, padx=2, pady=5)

    text4_button = tk.Button(root, text='Last week', command=partial(set_time, 3, start_time_entry, end_time_entry))
    text4_button.grid(row=3, column=0, padx=2, pady=5)

    text5_button = tk.Button(root, text='Last month', command=partial(set_time, 4, start_time_entry, end_time_entry))
    text5_button.grid(row=4, column=0, padx=2, pady=5)

    load_button = tk.Button(root, text='Load', width=10, command=partial(run, start_time_entry, end_time_entry, root))
    load_button.grid(row=4, column=2, padx=5, pady=5)

    return root
