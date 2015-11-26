#! /usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------
# 保证一个程序只有一个实例在运行。
# 例如，防止 crontab 调用两个程序实例。
#
# 使用方法：
# >>> import singleton
# >>> lockfile = "/tmp/<app>.lock"
# >>> instance = singleton.SingleInstance(lockfile)
# will sys.exit(-1) if other instance is running
#
# 参考：
# http://stackoverflow.com/questions/380870/python-single-instance-of-program
# https://github.com/ssbarnea/tendo/blob/master/tendo/singleton.py
# ----------------------------------------

import sys
import unittest
import fcntl


class SingleInstance(object):

    """
	If you want to prevent your script from running in parallel just
    instantiate SingleInstance() class. If is there another instance already
    running it will exist the application with the message "Another instance
    is already running, quitting.", returning -1 error code.

    This option is very useful if you have scripts executed by crontab
    at small amounts of time.

    Remember that this works by creating a lock file with a filename based
    on the full path to the script file.
    """
    def __init__(self, lockfile):
        self.lockfile = lockfile
        self.fp = open(self.lockfile, 'w')
        try:
            fcntl.lockf(self.fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except IOError:
            sys.exit(-1)

    def __str__(self):
        return "SingleInstance with lock file: %s" % self.lockfile


test_lock_file = "/tmp/test_lock_file.lock"
def f():
    instance = SingleInstance(test_lock_file)
    print instance


class testSingleton(unittest.TestCase):
    def test_1(self):
        instance = SingleInstance(test_lock_file)
        print instance

    def test_2(self):
        from multiprocessing import Process
        instance = SingleInstance(test_lock_file)
        print instance
        p = Process(target=f)
        p.start()
        p.join()
        # the called function should fail because we already have another
        # instance running note, we return -1 but this translates to 255
        # meanwhile we'll consider that anything different from 0 is good
        print p.exitcode
        assert(not p.exitcode == 0)


if __name__ == "__main__":
    unittest.main()
