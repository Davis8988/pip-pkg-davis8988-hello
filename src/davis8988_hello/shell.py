# Executes a command on windows CMD or unix Shell 

import subprocess

def execute(**kwargs):
    summary_dict = {"status" : False, "info" : ''}
    command_str = kwargs.get("command_str")  # Returns None if key not found
    command_timeout = kwargs.get("command_timeout")  
    if command_str is None:
        
        return summary_dict
    
    
    result = subprocess.run("dir /b", shell=True)
    print("Result:", result)    




