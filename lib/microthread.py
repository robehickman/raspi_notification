#!/usr/bin/env python

import collections
import time

class micro_thread(object):
    def main(self):
        pass

    def pass_config(self, name, conf):
        pass

    def setup(self):
        pass

thr = {}

def set_microthreads(t):
    global thr
    thr = t

def get_microthreads():
    global thr
    return thr

def call_on_thread(name, method, data):
    global thr
    return getattr(thr[name], method)(*data)

#Scheduler
def microthread_scheduler(active_microthreads):
    while 1:
        active_microthreads = sorted(active_microthreads, key=lambda t: t[0], reverse=True)

        cur_thread = active_microthreads.pop()

        if(cur_thread[0] > 0):
            time.sleep(cur_thread[0])

        pre_time = time.time()

        #Execute thread
        next_run = cur_thread[1].main()

        post_time = time.time()
        exec_time = post_time - pre_time

        next_run -= exec_time

        active_microthreads.append((next_run, cur_thread[1]))
        active_microthreads = sorted(active_microthreads, key=lambda t: t[0], reverse=True)


        try:
            if len(active_microthreads) > 0:
                next_thread = active_microthreads[-1]

                print next_thread
    
                time.sleep(next_thread[0])
    
                threads = []
                for t in active_microthreads:
                    threads.append((t[0] - next_thread[0], t[1]))
    
                active_microthreads = threads

        except IOError:
             pass
#            print cur_thread
#            print next_thread
#            print active_microthreads

