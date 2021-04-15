#!/usr/bin/python3 -u

# Sample the mic using SOX and print the max value of last N samples.
# EyC 13/04/2021
# 

import sys
import struct
import time
from math import sqrt
from subprocess import Popen, PIPE

#from file:
#cmdline = "/usr/bin/sox -V0 -q -e signed -b 16 -r 24k -c 1 -t raw ./soundsample.raw -r 8000 -b 16 -c 1 -t raw - highpass 100 sinc 50-2000 gain 10"

#from audio device:
cmdline = "/usr/bin/sox -V0 -q -t alsa hw:1 -r 8000 -b 16 -c 1 -t raw - highpass 20 noisered noise.prof 0.21 gain 30"

SR = 8000
secs = 5

maxsamples = SR * secs

nsamples = 0
sumsq = 0
maxvalue = 0

proc = Popen(cmdline, shell=True, stdin=PIPE, stdout=PIPE)

while True:
    twobytes = proc.stdout.read(2)
    if not twobytes:
        print("SOX terminated", file=sys.stderr)
        break;
    
    nsamples = nsamples + 1
    
    i = int.from_bytes(twobytes, byteorder='little', signed=True)
    #print(i)
    
    sumsq = sumsq + i*i
    maxvalue = max(abs(i), maxvalue)

    if nsamples >= maxsamples:
        print("{}\t{}\t{}\t{}".format(
            time.strftime('%Y/%m/%d-%H:%M:%S'),
            int(time.time()), 
            int(sqrt(sumsq/nsamples)), 
            maxvalue
        ))
        nsamples = 0
        sumsq = 0
        maxvalue = 0







# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
