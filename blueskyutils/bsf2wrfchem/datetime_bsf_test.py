#! usr/bin/env python 3

import datetime

file_name = '20130817'

yr = file_name[0:4]
mo = file_name[4:6]
d = file_name[6:8]

fmt = '%Y.%m.%d'
s = str(yr + '.' + mo + '.' + d)
dt = datetime.datetime.strptime(s, fmt)

tt = dt.timetuple()
tt.tm_yday

print(tt.tm_yday)