import paramiko
import logging


class RemoteWorker(object):
    '''Hook up a new puppet agent.
    
    This kind of blows because I have no separation between methods for
    the puppet master and the puppet agent... both are piggybacking on the
    same class for now.
    '''
    
    def __init__(self):
        self.client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.WarningPolicy)
        
        self.log = logging.getLogger(self.__module__ + '.' + self.__class__.__name__)
        
        self.hostname = None
        self.port = None
        self.username = None
        self.password = None
        
    def _get_provider(self):
        '''Return the path to the package manager for the distro.'''
        
        # dude this is fugly. this should probably be converted into a series
        # of try...except statements going through each known provider
        # indeedly, biggest problem is interacting with a remote system 
        # through paramiko... blargh!
        
        distro_probe = 'cat /etc/issue'
        stdin, stdout, stderr = self.client.exec_command('')
        
        output = stdout.read()
        self.log.info(output)
        self.log.error(stderr.read())
        
        if "Red Hat" in output:
            # assume nobody is going to try this on RHEL 4 and below
            provider = '/usr/bin/yum update -y'
        elif "Debian" in output:
            # does Ubuntu show up like this too?
            # what's the path to apt-get?
            provider = 'apt-get install'
        else:
            self.log.critical("Unsupported distro: {0}".format(output))
            
        return provider
        
    def _cmd(self, cmd):
        '''Run a single command on the system we're logged into'''
        
        (stdin, stdout, stderr) = self.client.exec_command(cmd)
        
        output = stdout.read()
        self.log.info(output)
        
        errors = stderr.read()
        self.log.error(errors)
        
        return (output, errors)
        
    def _privileged_cmd(self, cmd, password):
        '''Run a single privileged command on the system we're logged into
        with a password.
        
        Assumes cmd comes with a prefix that requires password input, like
        * sudo chmod FILE
        * su - -c cmod FILE
        
        Returns a tuple of stdout, stderr
        '''
        
        (stdin, stdout, stderr) = self.client.exec_command(cmd)
        stdin.write('{0}\n'.format(password))
        stdin.flush()
        
        output = stdout.read()
        self.log.info(output)
        
        errors = stderr.read()
        self.log.error(errors)
        
        return (output, errors)
    
    def set_creds(self, hostname, port=22, username=None, password=None):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        
    def clean_cert(self):
        '''Clean the certificate off the puppetmaster.
        Return a tuple of stdout, stderr.
        '''
        
        try:
            # connect
        
            # work
        
            # return (stdout, stderr)
        finally:
            self.client.close()

    def sign_cert_req(self):
        '''Sign the certificate request on the puppetmaster.
        Return a tuple of stdout, stderr.
        '''
        
        try:
            # connect
        
            # work
        
            # return (stdout, stderr)
        finally:
            self.client.close()
        
    def hookup_agent(self, cmd_prefix='', password=None, puppetargs=''):
        '''Hook a remote agent into a puppetmaster.
        
        Command prefix should be sudo or su if not logging in as root
        
        
        Return a tuple of stdout, stderr.
        '''
        
        install_ruby = '{0} {1} ruby rubygems'.format(cmd_prefix, provider)
        install_puppet = '{0} gem install puppet facter'.format(cmd_prefix)
        check_in = '{0} puppetd -t {1}'.format(cmd_prefix, puppetargs)
        

        try:
            # assume we've already set_creds
            self.client.connect(self.hostname, port=self.port, 
                                username=self.username, 
                                password=self.password)
        
            provider = self._get_provider()
        
            if cmd_prefix is None:
                self._cmd(install_ruby)
            else:
                self._privileged_cmd(install_ruby, password)
        
            # gem install puppet facter
        
            # try to check in
        finally:
            self.client.close()