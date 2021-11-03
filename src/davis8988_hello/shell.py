# Executes a command on windows CMD or unix Shell 

import root_logging
import subprocess
import time
from threading import Timer


get_root_logger_result_dict = root_logging.get_root_logger() 
if not get_root_logger_result_dict['result']:
    print(get_root_logger_result_dict['info'])  # This should occur on import failures - then printing & raising exceptions are required
    raise Exception(get_root_logger_result_dict['info']) 

root_logger = get_root_logger_result_dict['root_logger']


def _command_skip_printings(msg):
    pass

def _command_raise_timedout_exception(**kwargs):
    default_err_msg = "Executed command timed out"
    err_msg = kwargs.get("err_msg", default_err_msg) 
    process_obj = kwargs.get("process_obj", None) 
    if process_obj:
        print(f"Killing proc: {str(process_obj)}")
        process_obj.kill()
    raise TimeoutError(err_msg)

def execute(command_str, **kwargs):
    summary_dict = {"status" : True, "info" : '', 'exitcode': None, 'output': None}
    all_args_str = '\n'.join('='.join((key,str(val))) for (key,val) in kwargs.items())
    root_logger.debug(f'Received params:\n{all_args_str}')

    command_str                  = kwargs.get("command_str", command_str)  
    command_timeout_sec          = kwargs.get("command_timeout_sec")  
    command_cwd                  = kwargs.get("command_cwd")  
    command_redirect_stdout_to   = kwargs.get("command_redirect_stdout_to", subprocess.PIPE)  
    command_redirect_stderr_to   = kwargs.get("command_redirect_stderr_to", subprocess.STDOUT)  
    command_output_decode        = kwargs.get("command_output_decode", "utf-8")  
    command_hide_output          = kwargs.get("command_hide_output", False)  
    command_no_wait              = kwargs.get("command_no_wait", False)  

    # Check Mandatory params
    root_logger.debug('Checking mandatory params')
    if command_str is None:
        root_logger.debug("Missing mandatory param for function execute() : 'command_str' ")
        summary_dict['status'] = False
        summary_dict['info'] = "Missing mandatory param for function execute() : 'command_str' "
        return summary_dict
    
    # Assign command output printing func
    printing_func = root_logger.info
    if command_hide_output:
        printing_func = _command_skip_printings


    try:    
        root_logger.info(f"Executing: {command_str}")
        process_obj = subprocess.Popen(command_str, 
                                        shell=True, 
                                        stdout=command_redirect_stdout_to, 
                                        stderr=command_redirect_stderr_to,
                                        cwd=command_cwd )
        time.sleep(0.1)

        # No wait
        if command_no_wait:
            root_logger.debug("Not waiting for command to finish")
            return summary_dict  # When doesn't want to wait - Finish here
    
        # Wait for command to finish
        timer = None # Default - No timer
        if command_timeout_sec:
            root_logger.debug(f"Preparing timer of {command_timeout_sec} seconds and waiting for command to finish")
            callback_func_kwargs_dict = {'err_msg' : f'Executed command timed out after {command_timeout_sec} seconds', 'process_obj': process_obj}
            timer = Timer(command_timeout_sec, _command_raise_timedout_exception, [], callback_func_kwargs_dict)
            timer.start()  # Start the timer, and loop while waiting for command to finish
        
        proc_out = ''
        while process_obj.poll() is None:
            # print("Still waiting..")
            stdout = process_obj.stdout
            stderr = process_obj.stderr
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
    except BaseException as err_msg:
        root_logger.info(f"ERROR: {err_msg}")
        summary_dict['status'] = False
        summary_dict['info'] = err_msg
        return summary_dict
    finally:
        if timer is not None:
            root_logger.debug("Cancelling started command timer")
            timer.cancel()
    
    summary_dict["exitcode"] = process_obj.returncode
    summary_dict["output"] = proc_out
    return summary_dict


result = execute("asdadsas ping localhost -n 2", command_timeout_sec=5)
execute("ping localhost -n 10")


