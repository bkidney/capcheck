import sys
import subprocess
import yaml
import re
from sets import Set

fbsd_dir = sys.argv[1]

all = Set() 
allowed = Set()
disallowed = Set()

with open(fbsd_dir + "/sys/kern/capabilities.conf") as cap:
    for line in cap:
        if (not re.match('^[#\s]', line)):
            allowed.add(line.strip())

with open(fbsd_dir + "/sys/kern/syscalls.c") as calls:
    for line in calls:
        line = line.strip()
        syscalls = re.findall('"([^"]*)"', line)
        for syscall in syscalls:
            if (not re.match('^#', syscall)):
                all.add(syscall)

disallowed = all - allowed

for call in disallowed:
    print(call)

# elfdata = subprocess.check_output(['readelf', '-s', binary])
# elfdata = elfdata.split('\n')

# fns = []
# for line in elfdata:
#     if len(line.split()) > 8:
#         fn, lib = line.split()[7].split('@')

#         if (lib.startswith("FBSD")):
#             fns.append(fn)

# fns = list(dict.fromkeys(fns))

# print(fns)
