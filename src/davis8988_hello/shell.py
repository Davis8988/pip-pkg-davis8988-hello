# Executes a command on windows CMD or unix Shell 

import subprocess

def execute(**kwargs):
    command_str = kwargs.get("command_str")  # Returns None if key not found
    command_timeout = kwargs.get("command_timeout")  
    pass

result = subprocess.run("dir /b", shell=True)

print("Result:", result)

