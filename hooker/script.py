import paramiko
import argparse
import getpass

def get_distro():
    '''Return a string representing the distro we're on.'''
    
    pass
    
def get_provider():
    '''Return a string representing the path to which package manager we're on
    based on which distro we're on.'''
    
    pass

def install()

def 



"""
OK WTF are we doing here....

figure out some stuff first
* if we need to clean the cert off the puppetmaster first
* how we're going to authenticate
* what host we're trying to hook up
* if we want a specific version of puppet
* if we need to go sign the cert on the puppetmaster
if told, clean the cert off the puppetmaster first
ssh to a host
figure out what distro we're on to get a provider
use that provider to install ruby and rubygems
gem install puppet facter
try to check in
go to the puppetmaster and sign the cert

"""