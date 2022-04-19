import subprocess 
import time

try:
    print("Starting Server...")
    server_proc = subprocess.Popen('node server/index.js', shell=True)
    time.sleep(5.0)
    print("Openning Midi...")
    midi_proc = subprocess.Popen('py main.py 0', shell=True)

    while server_proc.returncode is None and midi_proc.returncode is None:
        server_proc.poll()
        midi_proc.poll()
    # if loop breaks, through error
    raise
except: 
    print("Closing Server...")
    server_proc.kill()
    print("Closing Midi...")
    midi_proc.kill()
