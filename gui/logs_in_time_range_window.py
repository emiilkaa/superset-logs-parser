import datetime
import tkinter as tk
from functools import partial
from tkinter import messagebox

from pandastable import addButton, Table

from gui.utils.save_utils import save_dataframe
from repository.log_repository import get_logs_between_datetimes

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
    if start and end:
        try:
            start_dttm = datetime.datetime.strptime(start, DATETIME_FORMAT)
            end_dttm = datetime.datetime.strptime(end, DATETIME_FORMAT)
            logs = get_logs_between_datetimes(start_dttm, end_dttm)
        except ValueError:
            messagebox.showerror('Invalid format', 'Please enter dates in format DD.MM.YYYY HH:mm:SS')
            return
        except Exception as e:
            messagebox.showerror('DB error', str(e), parent=parent)
            return
        table_root = tk.Toplevel(parent)
        table_root.title(f'Logs from {start} to {end}')
        table_root.geometry('1000x750')

        toolbar = tk.Frame(table_root)
        toolbar.pack()
        addButton(toolbar, 'Save results',
                  partial(save_dataframe, logs,
                          f'logs_from_{start_dttm.strftime("%Y%m%d%H%M%S")}_to_{end_dttm.strftime("%Y%m%d%H%M%S")}.csv',
                          table_root),
                  side='right')

        frame = tk.Frame(table_root)
        frame.pack(fill='both', expand=True)

        pt = Table(frame, dataframe=logs)
        pt.show()
    else:
        messagebox.showerror('Invalid request', 'Please enter all required parameters.', parent=parent)


def open_logs_in_time_range_window(master):
    root = tk.Toplevel(master)
    root.title('Get logs between dates')

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
