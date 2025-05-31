import tkinter as tk
import funFact, authorsNote, weather, trumpSummarizer
from credentials import TWITTER_USERNAME, TWITTER_PASSWORD
from seleniumPoster import post_tweet

def toggle_auto():
    if auto_button.cget('bg') == 'white':
        auto_button.config(bg='blue', fg='white')  # On state
        # TODO: Implement AUTO functionality
    else:
        auto_button.config(bg='white', fg='black')  # Off state
        # TODO: Implement AUTO functionality

# Create the main window
root = tk.Tk()
root.title("Twitter Yapper Bot")

# Title at the top
title = tk.Label(root, text="Twitter Yapper Bot", font=('Arial', 16))
title.pack(pady=10)

# Four main buttons
button_trump = tk.Button(
    root,
    text="What did Trump do today?",
    width=20,
    command=lambda: post_tweet(TWITTER_USERNAME, TWITTER_PASSWORD, trumpSummarizer.get_message())
)
button_trump.pack(pady=5)

button_weather = tk.Button(
    root,
    text="What's the weather like?",
    width=20,
    command=lambda: post_tweet(TWITTER_USERNAME, TWITTER_PASSWORD, weather.get_message())
)
button_weather.pack(pady=5)

button_funFact = tk.Button(
    root,
    text="Fun Fact",
    width=20,
    command=lambda: post_tweet(TWITTER_USERNAME, TWITTER_PASSWORD, funFact.get_message())
)
button_funFact.pack(pady=5)

button_authorsNote = tk.Button(
    root,
    text="Author's Note",
    width=20,
    command=lambda: post_tweet(TWITTER_USERNAME, TWITTER_PASSWORD, authorsNote.get_message())
)
button_authorsNote.pack(pady=5)


# Toggle button in the lower right corner
auto_button = tk.Button(root, text="AUTO", width=8, bg='white', command=toggle_auto)
auto_button.place(rely=1.0, relx=1.0, anchor='se', x=-10, y=-10)  # Lower right with small margin[3]

root.mainloop()
