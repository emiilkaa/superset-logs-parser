import tkinter as tk
from functools import partial
from tkinter import messagebox

from matplotlib import pyplot as plt

from gui.utils.save_utils import save_plot
from gui.utils.validate import digit_validation
from repository.log_repository import plot_dashboard_usage_by_month, plot_dashboard_usage_by_hour


def run(func, dashboard_id_entry, save_button, parent):
    dashboard_id = dashboard_id_entry.get()
    if dashboard_id:
        try:
            results = func(int(dashboard_id))
        except Exception as e:
            messagebox.showerror('DB error', str(e))
            return

        plt.show()
        filename = f'dashboard_{dashboard_id}_by_month.png'
        save_button.config(command=partial(save_plot, results, filename, parent), state=tk.NORMAL)
    else:
        messagebox.showerror('Invalid request', 'Please enter all required parameters.')


def open_plot_window(func, master):
    root = tk.Toplevel(master)
    root.title('Plot dashboard usages by month')
    root.geometry('650x150')

    id_frame = tk.Frame(root)
    id_frame.pack(side=tk.TOP, padx=10, pady=10)

    id_label = tk.Label(id_frame, text='Dashboard ID: ')
    id_label.pack(side=tk.LEFT)
    id_entry = tk.Entry(id_frame, validate='key', vcmd=(root.register(partial(digit_validation, root)), '%S'))
    id_entry.pack(side=tk.LEFT)

    button_frame = tk.Frame(root)
    button_frame.pack(side=tk.TOP, padx=10, pady=10)

    save_button = tk.Button(button_frame, text='Save results', state=tk.DISABLED)
    run_button = tk.Button(button_frame, text='Run', command=partial(run, func, id_entry, save_button, root))

    run_button.pack(side=tk.LEFT)
    save_button.pack(side=tk.LEFT, padx=15)

    return root


def open_plot_by_month_window(master):
    return open_plot_window(plot_dashboard_usage_by_month, master)


def open_plot_by_hour_window(master):
    return open_plot_window(plot_dashboard_usage_by_hour, master)
