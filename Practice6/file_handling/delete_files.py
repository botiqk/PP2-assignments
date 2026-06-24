import os

if os.path.exists("sample_backup.txt"):
    os.remove("sample_backup.txt")
    print("Backup deleted.")
else:
    print("File does not exist.")