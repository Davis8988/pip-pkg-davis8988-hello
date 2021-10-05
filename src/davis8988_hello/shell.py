# Executes a command on windows CMD or unix Shell 

import subprocess

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
    execute_result = subprocess.Popen(command_str, shell=True, stdin=None, stdout=None, stderr=None,)
    input("Waiting..")
    stdoutdata, stderrdata = execute_result.communicate()
    print("stdoutdata=", stdoutdata)
    print("stderrdata=", stderrdata)
    print("done")

    # print("Result:", result)    

execute("ping localhost -n 15")


