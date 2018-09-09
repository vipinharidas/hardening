#!/usr/bin/env python3.6
#
# server hardening by bipul.p <bipul_pr[at]live.com>
##

import subprocess,argparse,uuid,logging,re
from fabric.api import local,env,run,settings,hide, put
from fabric.tasks import execute

def check_fqdn(fdn):
	t = re.search(r'([a-zA-Z0-9]*\.[a-zA-Z0-9]*\.[a-zA-Z0-9]*$)',fdn) 
	if t:
		return fdn
	else:
		return ("server."+fdn)

def harden(t):
	if not run('ls -al /root/.hardened').failed or not local('ls -al /var/run/%s' % t.fqdn).failed:
		return 2
	
	#create a lock
	local('touch /var/run/%s' % t.fqdn)
	# create zip of current ansible files
	local('cd /opt/server.hardening/;rm -rf ansible-harden.zip; zip -9 -qr --exclude=*.git* --exclude=sub.py --exclude=*.retry --exclude=README.md ansible-harden.zip .')
	
	# install deps
	run('yum install epel-release wget unzip python-pip ansible -y')
	# drop zip at dest
	put('/opt/server.hardening/ansible-harden.zip', '/usr/local/src')
	run('unzip -oq /usr/local/src/ansible-harden.zip -d /usr/local/src/ansible; rm -f /usr/local/src/ansible-harden.zip')
	
	# pass passed args:
	# check mode
	if t.dr == True: 
		args = ('cd /usr/local/src/ansible/ && /usr/bin/ansible-playbook main.yml --connection=local --check -vvvv -e \"email=%s wheel_password=%s fqdn=%s ns1=%s ns2=%s\"' % (t.email,t.adminp,t.fqdn_1,t.ns1,t.ns2) )
	
	else:
		args = ('cd /usr/local/src/ansible/ && /usr/bin/ansible-playbook main.yml --connection=local -vvvv -e \"email=%s wheel_password=%s fqdn=%s ns1=%s ns2=%s\"' % (t.email,t.adminp,t.fqdn_1,t.ns1,t.ns2) )	

	y = run(args)
	logger.info(y)
	if not y.failed:
		run('rm -rf /usr/local/src/ansible-harden.zip /usr/local/src/ansible/')
		run('yum remove ansible -y')
		if t.dr == True:
			local('rm -rf /var/run/%s' % t.fqdn)
		else:
			run('touch /root/.hardened')
			run('shutdown -r now')
			local('rm -rf /var/run/%s' % t.fqdn)
			logger.info('%s going down for reboot!', t.host)
		return 1

	else:
		return 0


if __name__ == "__main__":

	try:
		# parse args
		parser = argparse.ArgumentParser()
		parser.add_argument('--host',dest='host',required=True)
		parser.add_argument('--rootp',dest='rootp',required=True)
		parser.add_argument('--email',dest='email',required=True)
		parser.add_argument('--fqdn',dest='fqdn',required=True)
		parser.add_argument('--dryrun',dest='dr',action='store_true')
		
		# gen admin pass
		t = parser.parse_args()

	except Exception as argerror:
		print(argerror.args)
#		logger.error(argerror.args)

	if t.fqdn:
		logfile='/var/log/hardening/'+t.fqdn
	else:
		logfile='/var/log/hardening/mainlog'
	
	logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(levelname)s %(message)s',filename=logfile)
	logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	logger = logging.getLogger('sdhn')
	
	logger.info('logging started for %s', t.host)	
	
	try:
		t.fqdn_1 = check_fqdn(t.fqdn)
		t.ns1 = "ns1."+t.fqdn
		t.ns2 = "ns2."+t.fqdn

		t.adminp = str(uuid.uuid1()).replace('-', '')[:-15]
		host = t.host
		env.user = "root"
		env.abort_on_prompts = False

		if t.rootp:
			env.password = t.rootp

		with hide('output','running','warnings'),settings(warn_only=True):
			results = execute(harden,t,hosts=host)
			# for debug purpose only
			#print (results)
			if results[t.host] == 1:
				if t.dr == True:
					print("Dryrun success!")
				else: 
					print("admin pass : %s"%t.adminp)
			if results[t.host] == 2:
				print("Already hardened or in process")
			
			if results[t.host] == 0:
				print("Failed at harden")

	except Exception as argerror:
		print(argerror.args)
		logger.error('hardening failed %s', argerror.args)
