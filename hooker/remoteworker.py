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
        
        # connect
        
        # work
        
        # return (stdout, stderr)

        pass

    def sign_cert(self):
        '''Sign the certificate request on the puppetmaster.
        Return a tuple of stdout, stderr.
        '''
        
        # connect
        
        # work
        
        # return (stdout, stderr)

        pass
        
    def hookup_agent(self):
        '''Hook a remote agent into a puppetmaster.
        Return a tuple of stdout, stderr.
        '''

        try:
            # assume we've already set_creds
            self.client.connect(self.hostname, port=self.port, 
                                username=self.username, 
                                password=self.password)
        
            provider = self._get_provider()
        
            # use that provider to install ruby and rubygems
        
            # gem install puppet facter
        
            # try to check in
        
        pass
    
    