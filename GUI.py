import tkinter as tk

def toggle_auto():
    if auto_button.cget('bg') == 'white':
        auto_button.config(bg='blue', fg='white')  # On state
    else:
        auto_button.config(bg='white', fg='black')  # Off state

# Create the main window
root = tk.Tk()
root.title("Twitter Yapper Bot")

# Title at the top
title = tk.Label(root, text="Twitter Yapper Bot", font=('Arial', 16))
title.pack(pady=10)

# Four main buttons (replace 'Option X' with your actual button names)
for i in range(1, 5):
    button = tk.Button(root, text=f"Option {i}", width=20)
    button.pack(pady=5)

# Toggle button in the lower right corner
auto_button = tk.Button(root, text="AUTO", width=8, bg='white', command=toggle_auto)
auto_button.place(rely=1.0, relx=1.0, anchor='se', x=-10, y=-10)  # Lower right with small margin[3]

root.mainloop()
