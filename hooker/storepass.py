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
        # clarify which password we're asking for
        if option_string == '--password':
            prompt = 'Password: '
        elif option_string == '--switch-user':
            prompt = 'Root password: '
        
        # get the password
        if values is None:
            password = getpass.getpass(prompt)
        else:
            password = values
            
        # store
        setattr(namespace, self.dest, password)