#!/usr/bin/env python
# ============================== SUMMARY =====================================
# Author : Paulo Celestino
# Date : 28/09/2020
# Version : 1.2
# Licence : GPL
# ===================== INFORMATION ABOUT THIS PLUGIN ========================
#
# This plugin checks Gearmand CLOSE_WAIT Status
#
# ========================== START OF PROGRAM CODE ===========================
import os, sys, subprocess

# Global
OK=0
WARNING=1
CRITICAL=2
UNKNOWN=3

# Threshold for alarm
warning= int(sys.argv[1])
critical= int(sys.argv[2])

def execute_command(commandstring):
    try:
        output = subprocess.Popen(commandstring,stdout=subprocess.PIPE)
        return(output)
    except Exception as e:
        msg = "Exception calling command: '%s' , Exception: %s" % (commandstring,str(e))
        return(msg)

result = execute_command(['gearman_top','-b']).stdout.readlines()

for line in result:
    if('failed' in line):
        total_jobs = 200
        print("Error - Gearman Total Jobs Running Return Failed  | Total Jobs Running=%d;%d;%d;" % (total_jobs,warning,critical))
        sys.exit(CRITICAL)

    if('interrupt' in line):
        total_jobs = 201
        print("Error - Gearman Total Jobs Running Return Interrupt | Total Jobs Running=%d;%d;%d;" % (total_jobs,warning,critical))
        sys.exit(CRITICAL)



total_jobs = 0

for i in range(4,len(result) - 1):
    cleanline = result[i].replace(' ','')
    chunks = cleanline.split('|')
    jobs = chunks[3].replace('\n','')
    total_jobs += int(jobs)

if(total_jobs > critical):
    print("Critical Gearman Total Jobs Running: %s | Total Jobs Running=%d;%d;%d;" % (total_jobs,total_jobs,warning,critical))
    sys.exit(CRITICAL)
elif(total_jobs > warning):
    print("Warning - Gearman Total Jobs Running: %s | Total Jobs Running=%d;%d;%d;" % (total_jobs,total_jobs,warning,critical))
    sys.exit(WARNING)
else:
    print("OK - Gearman Total Jobs Running: %s | Total Jobs Running=%d;%d;%d;" % (total_jobs,total_jobs,warning,critical))
    sys.exit(OK)