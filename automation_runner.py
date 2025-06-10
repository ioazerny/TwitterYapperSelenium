import time
import os
import sys
import subprocess
from credentials import TWITTER_USERNAME, TWITTER_PASSWORD
from seleniumPoster import post_tweet
import funFact, authorsNote, weather, trumpSummarizer

AUTO_FILE = 'auto_mode.txt'
LAST_RUN_FILE = 'last_run.txt'
INTERVAL_SECONDS = 60  # 1 minute for testing

def is_auto_enabled():
    try:
        with open(AUTO_FILE, 'r') as f:
            return f.read().strip() == 'ON'
    except FileNotFoundError:
        return False

def has_interval_passed():
    if not os.path.exists(LAST_RUN_FILE):
        return True
    with open(LAST_RUN_FILE, 'r') as f:
        last_run = float(f.read())
    return (time.time() - last_run) >= INTERVAL_SECONDS

def update_last_run():
    with open(LAST_RUN_FILE, 'w') as f:
        f.write(str(time.time()))

def run_automation():
    # Example: Post a fun fact on Twitter
    post_tweet(TWITTER_USERNAME, TWITTER_PASSWORD, funFact.get_message())

def setup_windows_task():
    """
    Sets up this script as a scheduled task in Windows Task Scheduler to run every minute.
    Only needs to be run once.
    """
    python_exe = sys.executable
    script_path = os.path.abspath(__file__)
    task_name = "TwitterYapperAutomation"
    # Combine python_exe and script_path into one string, both quoted
    tr_arg = f'"{python_exe}" "{script_path}"'
    cmd = [
        'schtasks', '/Create', '/SC', 'MINUTE', '/MO', '1',
        '/TN', task_name,
        '/TR', tr_arg,
        '/F'
    ]
    try:
        subprocess.run(cmd, check=True)
        print(f"Scheduled task '{task_name}' created successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to create scheduled task: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == '--setup':
        setup_windows_task()
    else:
        if is_auto_enabled() and has_interval_passed():
            run_automation()
            update_last_run()
