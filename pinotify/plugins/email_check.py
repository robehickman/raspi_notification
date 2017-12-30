from multiprocessing import Process, Queue
from imapclient import IMAPClient
import collections, time

from pinotify.module_system       import *
import pinotify.plugins.display as dsp

class email_check(module):
    def __init__(self):
        self.config = {}

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def pass_config(self, name, conf):
        """ Store configuration item """
        self.config[name] = conf

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def check_mail(self, account, q):
        server = IMAPClient(account['smtp_server'], account['smtp_port'], use_uid=True, ssl=True, timeout=10)
        server.login(account['smtp_username'], account['smtp_password'])
        folder_status = server.folder_status('Inbox', 'UNSEEN')
        unseen = int(folder_status['UNSEEN'])
        q.put(unseen)

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=
    def start_process(self):
        """ Repeatedly check servers for new mail and add to display queue """

        q = Queue()

        while True:
            try:
                for name, account in self.config.iteritems():
                    p = Process(target=self.check_mail, args=(account, q))
                    p.start(); p.join();
                    unseen = q.get()

                    print name
                    print unseen

                    if unseen == 'error': continue
                    else: pass

                    try:
                        with open('/etc/pinotify/prev/' + name, 'r') as f:
                            previous_unseen = int(f.read())
                    except:
                        raise
                        previous_unseen = unseen

                    #----
                    if unseen <= previous_unseen:
                        previous_unseen = unseen
                        dsp.display_queue.put({'display' : self.config[name]['display'],
                                               'method'  : 'delete_screen',
                                               'name'    : name})

                    elif unseen > previous_unseen:
                        mail_new = unseen - previous_unseen

                        msg = "%i new mail" % mail_new
                        if(mail_new > 1): msg += "s"
                        dsp.display_queue.put({'display' : self.config[name]['display'],
                                               'method'  : 'replace_screen',
                                               'name'    : name,
                                               'data'    : self.config[name]['abbreviation'] + ' ' + msg + "\n" + ''})

                    with open('/etc/pinotify/prev/' + name, 'w') as f:
                        f.write(str(previous_unseen))

                    server.logout()

                time.sleep(30)
            except:
                raise
                pass
