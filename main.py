import sys
import time
import subprocess

command_to_perform = sys.argv[1]
output_file = sys.argv[2]
restart = bool(sys.argv[3]) if len(sys.argv) > 3 else False
timeout = int(sys.argv[4]) if len(sys.argv) > 4 else None

start_time = time.time()
process = subprocess.Popen(command_to_perform,
                           shell=True,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT)
with open(output_file, 'w') as f:
    while True:
        line = process.stdout.readline()
        f.write(line.decode('utf-8'))

        if process.poll() is not None:
            if restart:
                process = subprocess.Popen(command_to_perform,
                                           shell=True,
                                           stdout=subprocess.PIPE,
                                           stderr=subprocess.STDOUT)
            else:
                break
        if timeout and (time.time() - start_time) > timeout:
            process.kill()
            break
