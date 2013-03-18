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
parser.add_argument('-V', '--puppet-version',
                    help="Specify a puppet version to pass to\
                         'gem install puppet -V'"
parser.add_argument('-P', '--port', type=int, help='Port to use on the agent')
parser.add_argument('-l', '--login-name', default='root',
                    help='User name to log into the agent with')
parser.add_argument('host', 
                    help='IP address or FQDN of agent to install puppet on')
parser.add_argument('-v', '--verbose', action='count', default=0,
                    help='Set verbosity. Use more times for more verbose.')
                    
args = parser.parse_args()


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


def main():
    '''Run me, Johnny!'''
    
    master = remoteworker.RemoteWorker()
    #master.set_creds()
    
    agent = remoteworker.RemoteWorker()
    agent.set_creds(**setup_agent_creds())
    
    #if args.clean_cert:
    #    master.clean_cert()
                
    if args.sudo is True:
        agent.prefix = 'sudo '
    elif args.switch_user is not None:
        agent.prefix = 'su - -c '
        agent.superpass = args.switch_user
            
    puppetd_args = ''
    
    agent.hookup_agent(cmd_prefix=prefix, puppetd_args)
    
    #if args.john_hancock is True:
    #    master.sign_cert_req()