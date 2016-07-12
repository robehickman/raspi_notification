#!/usr/bin/env python

import collections
import time

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Read configuration file into a dict
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def read_config(file):
    conf_file = ConfigParser.ConfigParser()
    conf_file.read(file)

    config = {}

    for section in conf_file.sections():
        sect = {}

        options = conf_file.options(section)

        for option in options:
            sect[option] = conf_file.get(section, option)
        config[section] = sect
    return config


## module class ##
class module(object):
    config   = {}

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Store configuration item
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def pass_config(self, name, conf):
        self.config[name] = conf

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Modules setup method, should be overridden
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def setup(self):
        pass

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Modules setup method, should be overridden
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def start_process(self):
        pass


modules = {}

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Set a dictionary of module objects
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def set_modules(m):
    global modules
    modules = m

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Get registered module objects
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def get_modules():
    global modules
    return modules

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Pass configuration values from config to the modules
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def pass_configuration(config):
    global modules

    print 'Passing configuration'
    for section in config:
        module = config[section]['module']
        modules[module].pass_config(section, config[section])

    print 'Running setup'
    for key in modules:
        modules[key].setup()

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Start module worker processes
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def start_workers():
    global modules

    print 'Starting workers'
    # begin worker processes after the whole system is configured
    for key in modules:
        modules[key].start_process()

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Call a named method on a registered module
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def call_on_module(name, method, data):
    global modules
    return getattr(modules[name], method)(*data)

