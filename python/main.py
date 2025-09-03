import tkinter as tk
from src.views.toolbar_config import get_default_toolbar_config

root = tk.Tk()
#print(get_default_menu_config())
menubar = tk.Menu(root)
root.config(menu=get_default_toolbar_config())
menu = get_default_toolbar_config()
root.mainloop()
