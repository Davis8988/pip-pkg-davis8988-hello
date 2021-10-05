# Executes a command on windows CMD or unix Shell 

import subprocess
import time

def execute(command_str, **kwargs):
    summary_dict = {"status" : False, "info" : ''}
    command_str = kwargs.get("command_str", command_str)  
    command_timeout = kwargs.get("command_timeout")  
    command_cwd = kwargs.get("command_cwd")  
    if command_str is None:
        summary_dict['info'] = "Missing mandatory param for function execute() : 'command_str' "
        return summary_dict
    
    # execute_result = subprocess.run(command_str, shell=True)
    print("Executing:", command_str)
    process = subprocess.Popen(command_str, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    time.sleep(0.1)
    while process.poll() is None:
        print("Still waiting..")
        stdout = process.stdout
        stderr = process.stderr
        if stdout:
            print([str(l) for l in stdout.read()])
        if stderr:
            print([str(l) for l in stderr.read()])
        print(stdout)
        time.sleep(1)

    print("done waiting")

    # print("Result:", result)    

execute("ping localhost -n 10")


