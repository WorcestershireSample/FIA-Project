import os
import time
import subprocess

def monitor_directory(directory):
    files = set(os.listdir(directory))  # Get initial file list
    while True:
        time.sleep(1)  # Pause for 1 seconds, may lower
        new_files = set(os.listdir(directory)) - files  # Get new files
        if new_files:  # If new files found
            new_files_str = ''.join(new_files)
            print(f"New file(s) found: {new_files_str}")
            files |= new_files  # Add new files to file list, probably not necessary but hey!
            result = subprocess.run([f'python3.10', 'path/to/script.py', 'path/to/image/{new_files_str}'], stdout=subprocess.PIPE)
            print(result.stdout.decode('utf-8'))


if __name__ == "__main__":
    monitor_directory(r"C:\Users\Popip\Desktop\demontesting")