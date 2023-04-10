import os
import sys
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
            result = subprocess.run([f'python3.10', 'OCRfunc.py', '{directory}/{new_files_str}'], stdout=subprocess.PIPE)
            print(result.stdout.decode('utf-8'))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 daemon.py /path/to/directory")
        print("Defaulting to: /var/www/foodingredientanalyzer.online/html/images")
        directory = '/var/www/foodingredientanalyzer.online/html/images'
        monitor_directory(directory)
        sys.exit(0)
    directory = sys.argv[1]
    monitor_directory(directory)

# to run this passively, use nohup python3 monitor.py /path/to/directory &