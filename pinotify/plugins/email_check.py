import collections
import time
from imapclient import IMAPClient

from pinotify.module_system       import *
import pinotify.plugins.display as dsp

class email_check(module):
    def __init__(self):
        self.servers   = {}
        self.config = {}

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def pass_config(self, name, conf):
        """ Store configuration item """
        self.config[name] = conf

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=
    def setup(self):
        pass

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=
    def start_process(self):
        """ Begin mail checking process """
        self.check_mail(dsp.display_queue)

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=
    def check_mail(self, display_queue):
        """ Repeatedly check servers for new mail and add to display queue """

        def connect_server(hostname, port, username, password):
            """ Connect to mail server """
            server = IMAPClient(hostname, port, use_uid=True, ssl=True)
            server.login(username, password)
            return server

        # do initial setup
        for name, account in self.config.iteritems():
            server = connect_server(
                account['smtp_server'],
                account['smtp_port'],
                account['smtp_username'],
                account['smtp_password'])

            previous = server.folder_status(account['mailbox'], 'UNSEEN')['UNSEEN']
    
            self.servers[name] = {
                'previous':  previous,
                'do_notify': False}

        # main checking loop
        while 1:
            time.sleep(30)

            print 'checking'

            for name, account in self.config.iteritems():
                server = connect_server(
                    account['smtp_server'],
                    account['smtp_port'],
                    account['smtp_username'],
                    account['smtp_password'])

                #self.servers[name]['server'] = server

                abriv_name = self.config[name]['abbreviation']
    
                folder_status = server.folder_status(self.config[name]['mailbox'], 'UNSEEN')
                unseen = int(folder_status['UNSEEN'])


                #if unseen < self.servers[name]['previous']:
                #    self.servers[name]['previous']  = unseen

                if(unseen == 0 or unseen <= self.servers[name]['previous']):
                    self.servers[name]['do_notify'] = False
                    self.servers[name]['previous']  = unseen

                elif(unseen > self.servers[name]['previous']):
                    self.servers[name]['do_notify'] = True
                    #self.servers[name]['previous']  = unseen

                if(self.servers[name]['do_notify'] == True):
                    mail_new = unseen - self.servers[name]['previous']

                    msg = "%i new mail" % mail_new
                    if(mail_new > 1):
                        msg = msg + "s"

                    display_queue.put({
                        'display' : self.config[name]['display'],
                        'method'  : 'replace_screen',
                        'name'    : name,
                        'data'    :  abriv_name + ' ' + msg + "\n" + '                 '})

                else:
                    display_queue.put({
                        'display' : self.config[name]['display'],
                        'method'  : 'delete_screen',
                        'name'    : name})

                server.logout()

