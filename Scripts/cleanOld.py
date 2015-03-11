import os
from glob import glob
import sys
from itertools import groupby

import re

DATE_REGEX=re.compile(r'^(\d{4})(\d{2})(\d{2})$')

class File():
    def __init__(self, filename, year, month, day):
        self.filename = filename
        self.year = year
        self.month = month
        self.day = day
    def __repr__(self):
        return self.filename

"""Deletes old files (usually backups) matching a pattern containing
one wildcard, which represents the date stored in YYYYMMDD format.

The files are kept if they are the newest backup of:
    * the last week
    * any week in the last month
    * any month in the last year
    * any year

So, it keeps daily backups for the last week, weekly backups
for the last month, monthly backups for the last year, and
yearly backups for files older than a year.

Note that when we say "the last year", it doesn't really mean
the last 365 days. When the new year rolls around, all the last
year's backups will be deleted, except for the latest one. This 
actually does not sound ideal, now that I think of it, but I've
already written it this way. Ah well."""
def cleanOld(pattern):
    directory = os.path.dirname(pattern)
    files = glob(pattern)

    filesToConsider = []

    for fname in files:
        thedate = fname.rsplit('/')[-1].split('.')[0][-8:]
        if not DATE_REGEX.match(thedate):
            sys.stderr.write("Skipping file %s" % fname)
            continue
        year = int(thedate[0:4])
        month = int(thedate[4:6])
        day = int(thedate[6:8])

        filesToConsider.append(File(fname, year, month, day))

    organized = {}
    for f in filesToConsider:
        organized.setdefault(f.year, [])
        organized[f.year].append(f)

    for year, files in organized.items():
        months = organized[year] = {}
        for f in files:
            months.setdefault(f.month, [])
            months[f.month].append(f)

    filesToDelete = set()

    for year in sorted(organized.keys())[:-1]:
        maxmonth = max(organized[year].keys())
        maxday = max(organized[year][maxmonth])
        for month in organized[year].values():
            for f in month:
                if not (f.month == maxmonth and f.day == maxday):
                    filesToDelete.add(f)

    if len(organized) > 0:
        maxYear = sorted(organized.keys())[-1]
        for month in organized[maxYear].values():
            maxday = max([f.day for f in month])

            weeks = {}

            for f in month:
                week = (f.day-1)//7
                weeks.setdefault(week, [])
                weeks[week].append(f)

            for week in weeks.values():
                week.sort(key = lambda f: f.day)
                for notNewestDay in week[:-1]:
                    filesToDelete.add(notNewestDay)

    for i in filesToDelete:
        print 'Deleting %s ' % (i.filename)
        os.unlink(i.filename)
                
if __name__ == '__main__':
    cleanOld(sys.argv[1])
