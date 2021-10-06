# Executes a command on windows CMD or unix Shell 

import subprocess
import time

def execute(command_str, **kwargs):
    summary_dict                 = {"status" : False, "info" : ''}
    command_str                  = kwargs.get("command_str", command_str)  
    command_timeout              = kwargs.get("command_timeout")  
    command_cwd                  = kwargs.get("command_cwd")  
    command_redirect_stdout_to   = kwargs.get("command_redirect_stdout_to", subprocess.PIPE)  
    command_redirect_stderr_to   = kwargs.get("command_redirect_stderr_to", subprocess.STDOUT)  
    command_output_decode        = kwargs.get("command_output_decode", "utf-8")  
    command_hide_output          = kwargs.get("command_hide_output", False)  
    if command_str is None:
        summary_dict['info'] = "Missing mandatory param for function execute() : 'command_str' "
        return summary_dict
    
    print(f"Executing: {command_str}")
    processObj = subprocess.Popen(command_str, shell=True, stdout=command_redirect_stdout_to, stderr=command_redirect_stderr_to)
    time.sleep(0.1)
    while processObj.poll() is None:
        print("Still waiting..")
        stdout = processObj.stdout
        stderr = processObj.stderr
        if stdout:
            for line in stdout:
                print(line.decode(command_output_decode).strip() )
        if stderr:
            for line in stderr:
                print("Stderr:", line.decode(command_output_decode).strip() )
        time.sleep(1)

execute("ping localhost -n 2 && asdj")


