import tkinter as tk
from tkinter import messagebox
import main

def send_tweet():
    choice = var.get()
    if choice == "weather":
        main.post_weather_tweet()
    elif choice == "trump":
        main.post_trump_tweet()
    elif choice == "author":
        main.post_authors_note_tweet()
    else:
        messagebox.showerror("Error", "Please select an option.")
        return
    messagebox.showinfo("Success", "Tweet posted!")

root = tk.Tk()
root.title("Twitter Bot GUI")

var = tk.StringVar()

tk.Label(root, text="Choose what to tweet:").pack()

tk.Radiobutton(root, text="Weather", variable=var, value="weather").pack(anchor=tk.W)
tk.Radiobutton(root, text="Trump Summary", variable=var, value="trump").pack(anchor=tk.W)
tk.Radiobutton(root, text="Author's Note", variable=var, value="author").pack(anchor=tk.W)

tk.Button(root, text="Send Tweet", command=send_tweet).pack(pady=10)

root.mainloop()
