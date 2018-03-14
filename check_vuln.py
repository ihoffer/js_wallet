from subprocess import PIPE, Popen, run
from shutil import copyfile
import time
import os
import re
import json

binary_file = 'wallet_mod'
byte_step = 100000

#pkg wallet.js --target node9-linux-x64

max_step = 200000
min_step = 10000

#building the list of addresses where a bit flip doesn't change output of the process
exceptions = []
try:
    with open('exceptions.txt', 'r') as exc:
        for l in exc.readlines():
            interval = l.strip().split(',')
            exceptions.extend(range(int(interval[0]), int(interval[1])))
except:
    print('Exceptions not loaded')
    pass

def replace_byte(f, offset):
    replace_with = os.urandom(current_step)
    f.seek(offset)
    f.write(replace_with)

def clone_binary():
    copyfile('wallet', binary_file)
    run(["chmod", "+x", binary_file])


def timeout_run(filename):
    p = Popen(filename, shell=True, stdout=PIPE)

    time.sleep(1)
    p.kill()
    out, err = p.communicate()
    return out

def check_output(output):
    fine = re.compile('.*\[LOG\]\..*')
    something_happened = re.compile('.*Something happened.*')
    we_have_log = re.compile('.*LOG.*')
    if something_happened.match(output):
        return('Something happened', output)
    elif fine.match(output):
        return('Everything\'s fine')
    elif we_have_log.match(output):
        return('We have log', output)
    else:
        return('Unknown error breaking code')

def run_and_check():
    output = timeout_run('./{}'.format(binary_file)).decode('ascii').replace(' ', '').replace('\n', '')
    return check_output(output)

size = os.path.getsize('wallet')
print('Size of file is: {}'.format(size))
offset = 0

current_step = max_step
while current_step >= min_step:
    print('Starting with step size: {}'.format(current_step))
    exc_f = open('exceptions.txt', 'a')
    while offset < (size - current_step):
        if offset in exceptions:
            offset += current_step
            continue
        clone_binary()
        with open(binary_file, "r+b") as f:
            replace_byte(f, offset)
        status = run_and_check()
        print('offset: {}, step: {}, status: {}'.format(offset, current_step, status))
        if status == 'Everything\'s fine':
            exceptions.extend(range(offset, offset + current_step - 1))
            exc_f.write('{},{}\n'.format(offset, offset + current_step - 1))
            print('Exception added')
        offset += current_step
    current_step = int(current_step / 2)
    offset = 0
    exc_f.close()
