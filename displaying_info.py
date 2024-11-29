import tkinter as tk

def display_info(info):
    root = tk.Tk()
    root.title("Tom's Assistant - Results")
    text_widget = tk.Text(root, wrap=tk.WORD, width=80, height=20)
    text_widget.insert(tk.END, info)
    text_widget.pack(expand=True, fill='both', padx=10, pady=10)
    close_button = tk.Button(root, text="Close", command=root.quit)
    close_button.pack(pady=10)
    root.mainloop()