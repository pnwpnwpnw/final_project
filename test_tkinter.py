import os

# Directory path
directory = "./data/classifiers/"

# Check if the directory exists
if os.path.exists(directory):
    # Set write permissions to the directory
    os.chmod(directory, 0o777)  # 0o777 corresponds to full permissions for owner, group, and others
    print("Write permissions granted to the directory:", directory)
else:
    print("Directory does not exist:", directory)
