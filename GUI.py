import tkinter as tk
import logging
import os

import funFact, authorsNote, weather, trumpSummarizer
from credentials import TWITTER_USERNAME, TWITTER_PASSWORD
from seleniumPoster import post_tweet

# --- Persistent State Management for AUTO Mode ---

AUTO_FILE = 'auto_mode.txt'

def set_auto_enabled(enabled: bool):
    with open(AUTO_FILE, 'w') as f:
        f.write('ON' if enabled else 'OFF')

def is_auto_enabled():
    try:
        with open(AUTO_FILE, 'r') as f:
            return f.read().strip() == 'ON'
    except FileNotFoundError:
        return False

# --- Logging Setup ---

logging.basicConfig(filename='auto_toggle.log', level=logging.INFO)

# --- GUI Functions ---

def toggle_auto():
    if auto_button.cget('bg') == 'white':
        auto_button.config(bg='blue', fg='white')  # On state
        set_auto_enabled(True)
        logging.info("AUTO enabled")
    else:
        auto_button.config(bg='white', fg='black')  # Off state
        set_auto_enabled(False)
        logging.info("AUTO disabled")

def post_and_exit(message_func):
    post_tweet(TWITTER_USERNAME, TWITTER_PASSWORD, message_func())
    root.destroy()

# --- Main Window ---

root = tk.Tk()
root.title("Twitter Yapper Bot")

# Title at the top
title = tk.Label(root, text="Twitter Yapper Bot", font=('Arial', 16))
title.pack(pady=10)

button_trump = tk.Button(
    root,
    text="What did Trump do today?",
    width=20,
    command=lambda: post_and_exit(trumpSummarizer.get_message)
)
button_trump.pack(pady=5)

button_weather = tk.Button(
    root,
    text="What's the weather like?",
    width=20,
    command=lambda: post_and_exit(weather.get_message)
)
button_weather.pack(pady=5)

button_funFact = tk.Button(
    root,
    text="Fun Fact",
    width=20,
    command=lambda: post_and_exit(funFact.get_message)
)
button_funFact.pack(pady=5)

button_authorsNote = tk.Button(
    root,
    text="Author's Note",
    width=20,
    command=lambda: post_and_exit(authorsNote.get_message)
)
button_authorsNote.pack(pady=5)

# Toggle button in the lower right corner
auto_button = tk.Button(root, text="AUTO", width=8, bg='white', command=toggle_auto)
auto_button.place(rely=1.0, relx=1.0, anchor='se', x=-10, y=-10)  # Lower right with small margin

# Set AUTO button state on startup based on persisted state
if is_auto_enabled():
    auto_button.config(bg='blue', fg='white')
else:
    auto_button.config(bg='white', fg='black')

root.mainloop()
