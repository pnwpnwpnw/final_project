import sys
import os

# Your condition here
def should_use_red_dashboard():
    # Replace with your actual condition
    s = input()
    if s == 1:
        True
    else:
        False
    # For example, based on the time of day:
    from datetime import datetime
    current_hour = datetime.now().hour
    return current_hour < 12

if should_use_red_dashboard():
    os.system(f"{sys.executable} dashboard_red.py")
else:
    os.system(f"{sys.executable} dashboard_green.py")
