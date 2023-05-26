import datetime
import os.path
from tkinter import filedialog, messagebox

import matplotlib.pyplot as plt
import pandas as pd


def save_text(result: str, default_filename: str = None, parent=None):
    if default_filename is None:
        default_filename = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

    extensions = [('JSON files', '*.json'), ('Text files', '*.txt'), ('All files', '*.*')]

    file_path = filedialog.asksaveasfilename(
        initialfile=default_filename,
        defaultextension=extensions,
        filetypes=extensions,
        parent=parent
    )

    if file_path:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(result)
        except Exception:
            messagebox.showerror('File I/O error', 'There was an error with file you selected.')


def save_dataframe(result: pd.DataFrame, default_filename: str = None, parent=None):
    if default_filename is None:
        default_filename = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

    extensions = [('CSV files', '*.csv'), ('Excel files', '*.xlsx'), ('All files', '*.*')]

    file_path = filedialog.asksaveasfilename(
        initialfile=default_filename,
        defaultextension=extensions,
        filetypes=extensions,
        parent=parent
    )

    if file_path:
        try:
            if os.path.splitext(file_path)[1] in ('.xlsx', '.xls'):
                result.to_excel(file_path)
            else:
                result.to_csv(file_path)
        except Exception as e:
            messagebox.showerror('File I/O error', 'There was an error with file you selected.')


def save_plot(result: plt, default_filename: str = None, parent=None):
    if default_filename is None:
        default_filename = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

    extensions = [('PNG files', '*.png'), ('PDF files', '*.pdf'), ('Vector graphics files', '*.svg')]

    file_path = filedialog.asksaveasfilename(
        initialfile=default_filename,
        defaultextension=extensions,
        filetypes=extensions,
        parent=parent
    )

    if file_path:
        try:
            result.savefig(file_path)
        except Exception:
            messagebox.showerror('File I/O error', 'There was an error with file you selected.')
