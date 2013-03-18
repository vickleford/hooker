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




Should we even be asking for a flag to explicitly clean the cert off the puppetmaster? Or should we just do it?
[root@overlord-n01 ~]# puppetca --clean dsflkjdsflkjsdflkjfsd 1>/dev/null
[root@overlord-n01 ~]# echo $?
0
[root@overlord-n01 ~]#