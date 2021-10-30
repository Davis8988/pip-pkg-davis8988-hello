# Executes a command on windows CMD or unix Shell 

import subprocess
import time
from threading import Timer

def execute(command_str, **kwargs):
    summary_dict                 = {"status" : False, "info" : '', 'exitcode': None, 'output': None}
    command_str                  = kwargs.get("command_str", command_str)  
    command_timeout_sec          = kwargs.get("command_timeout_sec")  
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
    processObj = subprocess.Popen(command_str, 
                                    shell=True, 
                                    stdout=command_redirect_stdout_to, 
                                    stderr=command_redirect_stderr_to,
                                    cwd=command_cwd )
    time.sleep(0.1)
    summary_dict['status'] = True
    if command_no_wait:
        return summary_dict  # When doesn't want to wait - Finish here
        
    proc_out = ''


    def _timedout(err_msg):
        raise TimeoutError(err_msg)

    timer = Timer(command_timeout_sec, _timedout(f'Executed command timed out after {command_timeout_sec} seconds'))
    try:
        timer.start()  # Start the timer, and loop while waiting for command to finish
        
        while processObj.poll() is None:
            # print("Still waiting..")
            stdout = processObj.stdout
            stderr = processObj.stderr
            if stdout:
                for line in stdout:
                    line = line.decode(command_output_decode).strip()
                    proc_out += line + "\n"  # Python automatically translates '\n' to the proper newline character for your platform
                    printing_func(line)
            if stderr:
                for line in stderr:
                    line = line.decode(command_output_decode).strip()
                    proc_out += line + "\n"
                    printing_func("Stderr:", line)
            time.sleep(1)
    finally:
        timer.cancel()
    
    summary_dict["exitcode"] = processObj.returncode
    summary_dict["output"] = proc_out
    return summary_dict
def skip_printings(msg):
    pass

result = execute("asdadsas ping localhost -n 2")
execute("ping localhost -n 10")


