"""
OK WTF are we doing here....

figure out some stuff first
* if we need to clean the cert off the puppetmaster first
* what to use to authenticate with
* what host we're trying to hook up
* if we want a specific version of puppet
* if we need to go sign the cert on the puppetmaster
if told, clean the cert off the puppetmaster first
figure out how to auth with what we got
ssh to a host
figure out what distro we're on to get a provider
use that provider to install ruby and rubygems
gem install puppet facter
try to check in
go to the puppetmaster and sign the cert

usage: 
hooker [-csSpx] [-f puppetmaster_config] [-e environment] [-P port] [-i identity_file] [-l user] host
-c cleans cert on the puppetmaster 
-s specifies to use sudo on the host
-S specifies a su - password to use
-p specified which password to log into the system with
-x specifies to sign the cert on the puppetmaster

"""


import os
import argparse
import configobj
import remoteworker

from storepass import StorePass


parser = argparse.ArgumentParser()

authtype = parser.add_mutually_exclusive_group()
authtype.add_argument('-s', '--sudo', action='store_true', default=False,
                    help='Use sudo on the server to be hooked up')
authtype.add_argument('-S', '--switch-user', action=StorePass, default=False,
                    help='Switch user to root on the server to be hooked up')

parser.add_argument('-p', '--password', nargs='?', action=StorePass,
                    help='Give the password to log into the client with')
# support this later
#parser.add_argument('-i', '--identity-file', 
#                    help='SSH key to log in to the agent with')

parser.add_argument('-c', '--clean-cert', action='store_true', default=False, 
                    help='Clean the cert on the puppetmaster first')
# should this be in the config instead?
#parser.add_argument('-x', '--john-hancock', action='store_true', default=False,
#                    help='Sign the certificate request on the puppetmaster')
                    
parser.add_argument('-f', '--config', 
                    default=os.path.expanduser('~/.config/hooker/config.ini'))
parser.add_argument('-e', '--environment', nargs='?',
                    help='Which environment to hook into on the puppetmaster')
parser.add_argument('-P', '--port', type=int, help='Port to use on the agent')
parser.add_argument('-l', '--login-name', 
                    help='User name to log into the agent with')
parser.add_argument('host', 
                    help='IP address or FQDN of agent to install puppet on')
parser.add_argument('-v', '--verbose', action='count', default=0,
                    help='Set verbosity. Use more times for more verbose.')
                    
args = parser.parse_args()


def main():
    '''Run me, Johnny!'''
    
    master = remoteworker.RemoteWorker()
    master.set_creds()
    
    agent = remoteworker.RemoteWorker()
    agent.set_creds()
    
    if args.clean_cert:
        master.clean_cert()
                
    if args.sudo is True:
        prefix = 'sudo '
    elif args.switch_user is not None:
        prefix = 'su - -c '
    else:
        prefix = ''
        
    password = ''
    puppetd_args = ''
    
    agent.hookup_agent(cmd_prefix=prefix, puppetd_args)
    
    if args.john_hancock is True:
        master.sign_cert_req()
    
    
    