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
    command_no_wait              = kwargs.get("command_no_wait", False)  

    # Check Mandatory params
    if command_str is None:
        summary_dict['info'] = "Missing mandatory param for function execute() : 'command_str' "
        return summary_dict
    
    # Assign printing func
    printing_func = print
    if command_hide_output:
        printing_func = skip_printings

    print(f"Executing: {command_str}")
    processObj = subprocess.Popen(command_str, shell=True, stdout=command_redirect_stdout_to, stderr=command_redirect_stderr_to)
    time.sleep(0.1)
    summary_dict['status'] = True
    if command_no_wait:
        return summary_dict
    while processObj.poll() is None:
        # print("Still waiting..")
        stdout = processObj.stdout
        stderr = processObj.stderr
        if stdout:
            for line in stdout:
                printing_func(line.decode(command_output_decode).strip() )
        if stderr:
            for line in stderr:
                printing_func("Stderr:", line.decode(command_output_decode).strip() )
        time.sleep(1)

def skip_printings(msg):
    pass

execute("ping localhost -n 2 && asdj")


