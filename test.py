import subprocess

proc = subprocess.Popen(['play', 'static/beep_hi.wav'])
try:
    res = proc.wait(timeout=5)
    print('res: {}'.format(res))
    
except subprocess.TimeoutEXpired:
    print('poll? {}'.format(proc.poll()))
    print("pid: {}".format(proc.pid))
    proc.terminate()
    outs, errs = proc.communicate()
    print('poll? {}'.format(proc.poll()))