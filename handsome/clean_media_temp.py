# -*- coding: utf-8 -*-
# remove all files of an expired modification date = mtime
# you could also use creation date (ctime) or last access date (atime)
# os.stat(filename) returns (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime)

import glob
import os
import time
from datetime import datetime, timedelta


if __name__ == '__main__':
    root = os.path.realpath(os.path.dirname(__file__))
    media_temp_files = os.path.join(root, '..', 'media', 'tmp', '*')

    for f in glob.glob(media_temp_files):
        # retrieves the stats for the current file
        # the tuple element at index 8 is the last-modified-date
        stats = os.stat(f)
        last_modify_date = time.localtime(stats[8])
        three_days_ago = datetime.now() - timedelta(days=3)
        if three_days_ago.timetuple() > last_modify_date:
            try:
                os.remove(f)
            except OSError:
                print 'Could not remove file', f
