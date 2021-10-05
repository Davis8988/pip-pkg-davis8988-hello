# Executes a command on windows CMD or unix Shell 

import subprocess

def execute(**kwargs):
    summary_dict = {"status" : False, "info" : ''}
    command_str = kwargs.get("command_str")  # Returns None if key not found
    command_timeout = kwargs.get("command_timeout")  
    command_cwd = kwargs.get("command_cwd")  
    if command_str is None:
        summary_dict['info'] = "Missing mandatory param for function execute() : 'command_str' "
        return summary_dict
    
    execute_result = subprocess.run(command_str, shell=True)
    print("Result:", result)    




