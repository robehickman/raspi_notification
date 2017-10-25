from multiprocessing import Process
import ConfigParser
import collections
import time

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def read_config(file):
    """ Read configuration file into a dict """

    conf_file = ConfigParser.ConfigParser()
    conf_file.read(file)

    config = {}
    for section in conf_file.sections():
        config[section] = {option : conf_file.get(section, option) for option in conf_file.options(section)}
    return config


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class module(object):
    def pass_config(self, name, conf):
        """ Store configuration item """
        pass

    def setup(self):
        """ Modules setup method, should be overridden """
        pass

    def start_process(self):
        """ Modules setup method, should be overridden """
        while True: time.sleep(10)

modules = {}

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def set_modules(m):
    """ Set a dictionary of module objects """
    global modules
    modules = m

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def get_modules():
    """ Get registered module objects """
    global modules
    return modules

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def pass_configuration(config):
    """ Pass configuration values from config to the modules """
    global modules

    print 'Passing configuration'
    for section in config:
        module = config[section]['module']
        modules[module].pass_config(section, config[section])

    print 'Running setup'
    for key in modules:
        modules[key].setup()

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
workers = {}
def start_workers():
    """ Start module worker processes """
    global modules, workers
    print 'Starting workers'

    for n, module in enumerate(itervalues(modules)):
        p = Process(target=module.start_process); p.start()
        workers[n] = (p, module) # Keep the process and the app to monitor or restart

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def check_workers():
    """ Check that workers are still running and restart if not """
    global workers

    new_workers = {}
    for n, worker in iteritems(workers):
        p, module = worker
        if not p.is_alive():
            np = Process(target=module.start_process); np.start()
            new_workers[n] = (p, module)
        else: 
            new_workers[n] = worker
    workers = new_workers

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def call_on_module(name, method, data):
    """ Call a named method on a registered module """
    global modules
    return getattr(modules[name], method)(*data)

