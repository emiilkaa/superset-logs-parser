import ctypes
import tkinter as tk
from functools import partial

from gui.all_logs_window import open_all_logs_window
from gui.count_users_window import open_count_users_window
from gui.dashboard_count_usage_window import open_dashboard_count_usage_window
from gui.dashboard_logs_window import open_dashboard_logs_window
from gui.duration_stats_window import open_duration_stats_window
from gui.json_len_window import open_json_len_window
from gui.last_logs_window import open_last_logs_window
from gui.log_by_id_window import open_log_by_id_window
from gui.logs_in_time_range_window import open_logs_in_time_range_window
from gui.plot_windows import open_plot_by_month_window, open_plot_by_hour_window
from gui.popular_actions_window import open_popular_actions_window
from gui.unused_dashboards_window import open_unused_dashboards_window
from gui.user_actions_window import open_user_logs_window
from gui.users_popular_dashboards_window import open_users_popular_dashboards_window
from repository.db import session, engine

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except:
    ctypes.windll.user32.SetProcessDPIAware()

buttons = [
    {'text': 'Get log by ID', 'command': open_log_by_id_window, 'column': 0, 'row': 0},
    {'text': 'Get all logs', 'command': open_all_logs_window, 'column': 0, 'row': 1},
    {'text': 'Get last N logs', 'command': open_last_logs_window, 'column': 0, 'row': 2},
    {'text': 'Get logs between dates', 'command': open_logs_in_time_range_window, 'column': 0, 'row': 3},
    {'text': 'Get logs by dashboard', 'command': open_dashboard_logs_window, 'column': 0, 'row': 4},
    {'text': 'Count dashboards usage', 'command': open_dashboard_count_usage_window, 'column': 1, 'row': 0},
    {'text': 'Get last dashboards usage', 'command': open_unused_dashboards_window, 'column': 1, 'row': 1},
    {'text': 'Get user\'s actions', 'command': open_user_logs_window, 'column': 1, 'row': 2},
    {'text': 'How many users use each dashboard', 'command': open_count_users_window, 'column': 1, 'row': 3},
    {'text': 'Get stats by duration', 'command': open_duration_stats_window, 'column': 1, 'row': 4},
    {'text': 'Plot dashboard usages by month', 'command': open_plot_by_month_window, 'column': 2, 'row': 0},
    {'text': 'Plot dashboard usages by hour', 'command': open_plot_by_hour_window, 'column': 2, 'row': 1},
    {'text': 'Average size of extra data', 'command': open_json_len_window, 'column': 2, 'row': 2},
    {'text': 'Get popular actions by dashboards', 'command': open_popular_actions_window, 'column': 2, 'row': 3},
    {'text': 'Which dashboards users use', 'command': open_users_popular_dashboards_window, 'column': 2, 'row': 4},
]

root = tk.Tk()
root.title('Dashboard Tool')
root.geometry('700x270')

for button in buttons:
    new_button = tk.Button(root, text=button['text'], command=partial(button['command'], root))
    new_button.grid(column=button['column'], row=button['row'], sticky='ew', padx=5, pady=5)

root.mainloop()

session.close()
engine.dispose()
