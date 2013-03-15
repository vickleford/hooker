'''
Create a custom action for argparse aimed at getting a password safely
with the getpass module by specifying a single flag. For example, 
specifying -p should launch getpass.getpass() and store the value
without ever printing the password to stdout or leaving it for the vultures
in .bash_history.
'''


import getpass
import argparse

class StorePass(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if values is None:
            password = getpass.getpass()
        else:
            password = values
        setattr(namespace, self.dest, password)