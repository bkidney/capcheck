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
            if line.strip().startswith("sys_"):
                allowed.add(line.strip()[4:])

with open(fbsd_dir + "/sys/kern/syscalls.c") as calls:
    for line in calls:
        line = line.strip()
        syscalls = re.findall('"([^"]*)"', line)
        for syscall in syscalls:
            if (not re.match('^#', syscall)):
                all.add(syscall)

disallowed = all - allowed

# Hack to deal with libc aliasing syscalls
aliases = Set()
for fn in disallowed:
    fn = "_" + fn
    aliases.add(fn)
disallowed = disallowed.union(aliases)

for call in disallowed:
    print(call)

