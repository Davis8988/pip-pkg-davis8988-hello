# Executes a command on windows CMD or unix Shell 

import subprocess
result = subprocess.run("dir /b", shell=True)

print("Result:", result)

