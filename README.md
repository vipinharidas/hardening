# README #

Typical README.

### What is this for? ###

* Automate server.hardening process
* Reduce manual input to zero for dedicated server orders.

### Requirements ###

  - Python 3.6
  - pip3
  - ansible 
  - fabric3


### Usage ###

```
#!python
python sub.py --host <serverip> --rootp <root password> --email <customer's email> 
```

--host  - IP address of the server

--rootp - Root password for the server, use single quotes('') if it contains additional characters. 

--email - customer's email - used for notifications

--dryrun - do a dry run

### How it works ###

sub.py 
   - takes all the variables, processes them.
   - make connecting with remote server - install epel,ansible
   - deploys ansible code
   - starts ansible
   
main.yml
   - run and execute server.hardening role
   
# Why Ansible runs local mode ? #
To avoid clash during multiple orders in queue. Ansible will always run at server with host=localhost.

### What's more in future? ###
- Optimization of Apache/MySQL based on server plan.
- Installation of Engintron(Nginx Caching) - better protection against random hits,
- CSF DDOS protection -- check the feasibility of CSF's portflood and connlimit settings, 
- Exim/Spamassassin filters -- optimize exim filters to filter incoming/outgoing spam better like LSH, it should help in fixing IP rep issues.
- Integrate monitoring/metrics collection