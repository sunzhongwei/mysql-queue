#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------
# Description
#
# usage:
# python worker.py --worker=1
# python worker.py --worker=2
# ----------------------------------------
import torndb
import time
import datetime
import argparse
import singleton


WAIT = 5
MYSQL_HOST = "localhost"
MYSQL_DATABASE = "mysql_queue"
MYSQL_USER = "username"
MYSQL_PASSWORD = "password"

DB = torndb.Connection(
    host=MYSQL_HOST,
    database=MYSQL_DATABASE,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD)


class Worker(object):

    def __init__(self, worker_id):
        self.db = DB
        self.worker_id = worker_id
        self.task = None

    def fetch_new_task(self):
        '''Return True if new task exists.
        '''
        row_count = self.db.update('''
            UPDATE task_queue
            SET status = 'processing', worker_id = %s
            WHERE status = 'unprocess'
            ORDER BY id ASC
            LIMIT 1
        ''' % (self.worker_id, ))

        if row_count > 0:
            self.get_task()
            return True
        else:
            return False

    def fetch_interrupted_task(self):
        '''Return true if interrupted task exists.
        '''
        self.get_task()

        if self.task:
            return True
        else:
            return False

    def get_task(self):
        task = self.db.get('''
            SELECT id, msg_id FROM task_queue
            WHERE status = 'processing' AND worker_id = %s
        ''' % (self.worker_id, ))

        if task:
            self.task = {"msg_id": task.msg_id, "task_id": task.id}
        else:
            self.task = None

    def handle_task(self):
        print "handling msg id: %s" % self.task["msg_id"]
        time.sleep(3)
        print "finished msg id: %s" % self.task["msg_id"]
        DB.update('''
            UPDATE task_queue
            SET status = 'processed', finished_at = '%s'
            WHERE `id` = %s
        ''' % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
               self.task["task_id"]))

    def run(self):
        if self.fetch_interrupted_task():
            print "handling interrupted task"
            self.handle_task()

        while True:
            if self.fetch_new_task():
                self.handle_task()
            else:
                print "no new task, wait %s seconds to detect new task" % WAIT
                time.sleep(WAIT)


if '__main__' == __name__:
    parser = argparse.ArgumentParser()
    parser.add_argument('--worker', help='worker id, integer only.', type=int)
    args = parser.parse_args()

    if args.worker:
        print "current worker id: %s" % (args.worker, )
        lockfile = "/tmp/mysql-queue-worker-%s.lock" % args.worker
        instance = singleton.SingleInstance(lockfile)

        worker = Worker(worker_id=args.worker)
        worker.run()
    else:
        parser.print_help()
        print "invalid worker id, exit."
