#!/usr/bin/env python
 
from multiprocessing import Process, Queue
import collections
import time
from imapclient import IMAPClient

from microthread import *
import display

class email_check(micro_thread):
    servers   = {}
    accounts = {}

    def connect_server(self, hostname, port, username, password):
        server = IMAPClient(hostname, port, use_uid=True, ssl=True)
        server.login(username, password)
        return server

    def pass_config(self, name, conf):
    self.accounts[name] = conf

    def setup(self):
        for name, account in self.accounts.iteritems():
            server = self.connect_server(
                account['smtp_server'],
                account['smtp_port'],
                account['smtp_username'],
                account['smtp_password'])

            folder_status = server.folder_status(account['mailbox'], 'UNSEEN')
            previous = folder_status['UNSEEN']
    
            self.servers[name] = {
                'server':    server,
                'previous':  previous,
                'do_notify': False}

    def start_process():
        self.check_queue = Queue()
        p = Process(target=self.check_mail, args=(self.check_queue, display.display_queue))
        p.start()

    def main(self):
        #self.check_queue.put('check')
        return 30 # run in 30 seconds

    def check_mail(self, check_queue, display_queue):
        while 1:
            #check_queue.get()
            time.sleep(30)

            print 'checking'

            for name, account in self.accounts.iteritems():
                try:
                    server = self.connect_server(
                        account['smtp_server'],
                        account['smtp_port'],
                        account['smtp_username'],
                        account['smtp_password'])

                    self.servers[name]['server'] = server

                except (KeyboardInterrupt, SystemExit):
                    raise
                except:
                    print('Connection Timed out')

            for name, srv in self.servers.iteritems():
                try:
                    abriv_name = self.accounts[name]['abbreviation']
                    server = srv['server']
        
                    folder_status = server.folder_status(self.accounts[name]['mailbox'], 'UNSEEN')
                    unseen = int(folder_status['UNSEEN'])
    
                    mail_new = unseen - self.servers[name]['previous']

                    if(unseen == 0 or unseen <= self.servers[name]['previous']):
                        self.servers[name]['do_notify'] = False
                        self.servers[name]['previous']  = unseen

                    if(unseen > 0 and unseen > self.servers[name]['previous']):
                        self.servers[name]['do_notify'] = True

                    if(self.servers[name]['do_notify'] == True):

                        msg = "%i new mail" % mail_new
                        if(mail_new > 1):
                            msg = msg + "s"

                        display_queue.put({
                            'display' : self.accounts[name]['display'],
                            'method'  : 'replace_screen',
                            'name'    : name,
                            'data'    :  abriv_name + ' ' + msg + "\n" + '                 '})

                    else:
                        display_queue.put({
                            'display' : self.accounts[name]['display'],
                            'method'  : 'delete_screen',
                            'name'    : name})

                    #clear state
                    # if clear state button press, clear notify and update unseen counter

                    server.logout()

                except (KeyboardInterrupt, SystemExit):
                    raise
                except:
                    print('Connection Timed out')


