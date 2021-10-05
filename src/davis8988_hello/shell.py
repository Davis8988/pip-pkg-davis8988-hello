# Executes a command on windows CMD or unix Shell 

import subprocess

def execute(**kwargs):
    cmndStr = kwargs.get("command_str")  # Returns None if key not found
    pass

result = subprocess.run("dir /b", shell=True)

print("Result:", result)

