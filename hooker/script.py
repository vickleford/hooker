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
hooker [-csSp] [-f puppetmaster_config] [-e environment] [-P port] [-i identity_file] [-l user] host
-c cleans cert on the puppetmaster 
-s specifies to use sudo on the host
-S specifies a su - password to use
-p specified which password to log into the system with

"""


import os
import paramiko
import argparse
import getpass
import configobj


parser = argparse.ArgumentParser()
parser.add_argument('-c', '--clean', action='store_true', default=False, 
                    help='Clean the cert on the puppetmaster first')
parser.add_argument('-s', '--sudo', action='store_true', default=False,
                    help='Use sudo on the server to be hooked up')
parser.add_argument('-S', '--su-pw' action='store_true', default=False,
                    help='Give a su - password to use')
parser.add_argument('-p', '--password', action='store_true', default=False,
                    help='Give the password to log into the target client with')
args = parser.parse_args()


def get_distro():
    '''Return a string representing the distro we're on.'''
    
    pass
    
    
def get_provider():
    '''Return a string representing the path to which package manager we're on
    based on which distro we're on.'''
    
    pass


