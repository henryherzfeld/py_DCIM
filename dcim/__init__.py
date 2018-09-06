from __future__ import print_function
import copy
import netsnmp
from time import time
from time import sleep
import sys
from datetime import datetime
import dcim


act_int = dcim.interval
dcim.eprint(dcim.getDateTime(), "\nStarting Data Center Monitoring...\n")
print("Interval Time :", act_int, " sec /", round((act_int / 60.0), 2), " min")
EarliestDate = dcim.getEarliestDate()
print("Oldest Date       :", EarliestDate)


while True:
    exec('../conf.yaml')
    gatherLoop(EarliestDate)
