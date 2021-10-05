# Executes a command on windows CMD or unix Shell 

import subprocess

def execute(**kwargs):
    pass

result = subprocess.run("dir /b", shell=True)

print("Result:", result)

