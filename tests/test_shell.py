# Tests 'shell' module

import davis8988_hello.shell as myshell
import os

os.environ['LOGLEVEL'] = 'info'
result = myshell.execute("asdadsas ping localhost -n 2", command_timeout_sec=5)
myshell.execute("ping localhost -n 10")


