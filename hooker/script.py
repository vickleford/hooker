import os
import sys
import argparse
import configobj
import keyring
import getpass

import remoteworker
from storepass import StorePass


def setup_args():
    '''Return an argparse object for the main entry point.'''
    
    parser = argparse.ArgumentParser()

    parser.add_argument('-p', '--password', nargs='?', action=StorePass,
                        help='Give the password to log into the client with')
    # support this later
    # this is another good place for a mutually exclusive group with -p
    #parser.add_argument('-i', '--identity-file', 
    #                    help='SSH key to log in to the agent with')

    authtype = parser.add_mutually_exclusive_group()
    authtype.add_argument('-s', '--sudo', action='store_true', default=False,
                        help='Use sudo on the server to be hooked up')
    authtype.add_argument('-S', '--switch-user', action=StorePass, default=False,
                        help='Switch user to root on the server to be hooked up')

    parser.add_argument('-f', '--config', 
                        default=os.path.expanduser('~/.config/hooker/config.ini'),
                        help='Specify an alternate config file to load \
                              puppetmasters from.')
    parser.add_argument('-e', '--environment',
                        help='Which environment to hook into on the puppetmaster')
    parser.add_argument('-V', '--puppet-version',
                        help="Specify a puppet version to pass to\
                             'gem install puppet -V'")
    parser.add_argument('-P', '--port', type=int, help='Port to use on the agent')
    parser.add_argument('-l', '--login-name', default='root',
                        help='User name to log into the agent with')

    parser.add_argument('-c', '--clean-cert', action='store_true', default=False, 
                        help='Clean the cert on the puppetmaster first')
    # should this be in the config instead?
    #parser.add_argument('-x', '--john-hancock', action='store_true', default=False,
    #                    help='Sign the certificate request on the puppetmaster')
    parser.add_argument('-v', '--verbose', action='count', default=0,
                        help='Set verbosity. Use more times for more verbose.')

    parser.add_argument('puppetmaster',
                        help='Specify which puppetmaster from config to use')
    parser.add_argument('host', 
                        help='IP address or FQDN of agent to install puppet on')
                    
    return parser.parse_args()
    

def setup_passwd_args():
    '''Return an argparse object for the passwd entry point.'''
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--config', 
                        default=os.path.expanduser('~/.config/hooker/config.ini'),
                        help='Specify an alternate config file to load \
                              puppetmasters from.')
    parser.add_argument('puppetmaster',
                        help='Specify which puppetmaster from config to use')
    return parser.parse_args()
    
    
def setup_agent_creds():
    '''Return a dict of login credentials trnaslated from command line 
    arguments that we can pass to a RemoteWorker object.'''
    
    creds = { 
              'hostname': args.host,
              'port': args.port,
              'username': args.login_name, 
              'password': args.password
            }
    
    return creds


def setup_master_creds(file, section):
    '''Return a dict of login credentials translated from saved INI file
    and keyring.'''
        
    config = configobj.ConfigObj(file)
    
    try:
        hostname = config[section]['fqdn']
    except KeyError:
        sys.exit("Can't find the puppetmaster {0} in {1}".format(section,file))
        
    user = config[section].setdefault('user', os.getlogin())
                
    try:
        password = keyring.get_password(section, user)
    except:
        sys.exit("Could not load password for {0}".format(section))
        
    if password is None:
        sys.exit("Could not load password for {0}".format(section))
              
    creds = { 'hostname': hostname,
               'port': int(config[section].setdefault('port', 22)),
               'username': user,
               'password': password }
    
    return creds
    
    
def main():
    '''Run me, Johnny!'''
    args = setup_args()
    config = configobj.ConfigObj(args.config)
    config[args.puppetmaster].setdefault('wait_for_cert', 60)
    
    master = remoteworker.RemoteWorker()
    master.set_creds(setup_master_creds(args.config, args.puppetmaster))
    
    agent = remoteworker.RemoteWorker()
    agent.set_creds(**setup_agent_creds())
    
    #if args.clean_cert:
    #    master.clean_cert()
                
    if args.sudo is True:
        agent.prefix = 'sudo '
    elif args.switch_user is not None:
        agent.prefix = 'su - -c '
        agent.superpass = args.switch_user
        
    gem_args = []
    if args.puppet_version:
        gem_args.append('-v')
        gem_args.append(args.puppet_version)
    
    puppet_args = []
    puppet_args.append('--server')
    puppet_args.append(config[args.puppetmaster]['fqdn'])
    puppet_args.append('--waitforcert')
    puppet_args.append(config[args.puppetmaster]['wait_for_cert'])
    if args.environment:
        puppet_args.append('-e')
        puppet_args.append(args.environment)
    if 
    
    
    agent.hookup_agent(gemargs, puppetargs)
    
    #if args.john_hancock is True:
    #    master.sign_cert_req() 
    
    
def set_password():
    '''Set a password for a puppetmaster.'''

    args = setup_passwd_args()
    config = configobj.ConfigObj(args.config)
    
    username = config[args.puppetmaster]['user']
    password = getpass.getpass('New password: ')
    password2 = getpass.getpass('Retype password: ')
    
    if password == password2:
        keyring.set_password(args.puppetmaster, username, password)
    else:
        print("Passwords didn't match!")