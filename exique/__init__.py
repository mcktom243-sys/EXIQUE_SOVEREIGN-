import subprocess
import os

def check_process(name):
    # Sniff for the process
    check = subprocess.run(["pgrep", "-f", name], capture_output=True)
    return check.returncode == 0

def sleep(seconds):
    import time
    time.sleep(seconds)

