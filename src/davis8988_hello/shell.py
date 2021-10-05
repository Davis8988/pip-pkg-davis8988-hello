# Executes a command on windows CMD or unix Shell 

import subprocess

def execute(**kwargs):
    result_dict = {"status" : False, "info" : ''}
    command_str = kwargs.get("command_str")  # Returns None if key not found
    command_timeout = kwargs.get("command_timeout")  
    if command_str is None:
        print("Error - Missing mandatory param for function execute() : 'command_str' ")
        return None
    
    result = subprocess.run("dir /b", shell=True)
    print("Result:", result)    




