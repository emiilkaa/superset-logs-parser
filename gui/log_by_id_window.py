import tkinter as tk
from functools import partial
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText

from gui.utils.save_utils import save_text
from gui.utils.validate import digit_validation
from repository.log_repository import get_log_by_id


def run(dashboard_id_entry, result_text, save_button, parent):
    dashboard_id = dashboard_id_entry.get()
    if dashboard_id:
        try:
            results = get_log_by_id(int(dashboard_id))
        except Exception as e:
            result_text.configure(state=tk.NORMAL)
            result_text.delete('1.0', tk.END)
            result_text.configure(state=tk.DISABLED)
            messagebox.showerror('DB error', str(e))
            return
        result_text.configure(state=tk.NORMAL)
        result_text.delete('1.0', tk.END)
        result_text.insert(tk.END, results)
        result_text.configure(state=tk.DISABLED)

        filename = f'log_{dashboard_id}.json'
        save_button.config(command=partial(save_text, results, filename, parent), state=tk.NORMAL)
    else:
        result_text.configure(state=tk.NORMAL)
        result_text.delete('1.0', tk.END)
        result_text.configure(state=tk.DISABLED)
        messagebox.showerror('Invalid request', 'Please enter all required parameters.')


def open_log_by_id_window(master):
    root = tk.Toplevel(master)
    root.title('Get log by ID')
    root.geometry('650x700')

    id_frame = tk.Frame(root)
    id_frame.pack(side=tk.TOP, padx=10, pady=10)

    id_label = tk.Label(id_frame, text='Dashboard ID: ')
    id_label.pack(side=tk.LEFT)
    dashboard_id = tk.Entry(id_frame, validate='key', vcmd=(root.register(partial(digit_validation, root)), '%S'))
    dashboard_id.pack(side=tk.LEFT)

    result_frame = tk.Frame(root)
    result_frame.pack(side=tk.TOP, padx=10, pady=10)

    result_label = tk.Label(result_frame, text='Result:')
    result_label.pack(side=tk.TOP)
    result_text = ScrolledText(result_frame, height=27, state=tk.DISABLED)
    result_text.pack(side=tk.TOP)

    button_frame = tk.Frame(root)
    button_frame.pack(side=tk.TOP, padx=10, pady=10)

    save_button = tk.Button(button_frame, text='Save results', state=tk.DISABLED)
    run_button = tk.Button(button_frame, text='Run', command=partial(run, dashboard_id, result_text, save_button, root))

    run_button.pack(side=tk.LEFT)
    save_button.pack(side=tk.LEFT, padx=15)

    return root
