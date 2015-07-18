import re
from datetime import datetime

def getStartTime(sched):
    start = re.sub(r"[th,st,nd]", "", sched[sched.find(":")+1:]).strip()
    date = datetime.strptime(start, "%d %b %Y %H:%M:%S")
    return date

def nameMatch(namelist, string):
    for name in namelist:
        if (name in string.lower()):
            return True
    return False
