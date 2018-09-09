#!/bin/sh
if [ ! -d /var/log/sysmon ]
then
        mkdir -p /var/log/sysmon
fi
LOGDIR='/var/log/sysmon'
LD=`cat /proc/loadavg | awk '{print $1}'`
MEM=$(free -m|awk '{if(NR==2){pmem=$3/$2;if(pmem > 80){print 1}else{print 0}}}')

DATE=`date +%H%M`
DATE2=`date +%b%d`


if [ $(echo "$LD>10" | bc) -eq 1 ] || [ $MEM -eq 1 ]
then
        if [ ! -d $LOGDIR/$DATE2 ]
        then
                mkdir -p $LOGDIR/$DATE2
        fi
        netstat -npt > $LOGDIR/$DATE2/nw_$DATE.txt
        ps -aufwx > $LOGDIR/$DATE2/ps_$DATE.txt
        /usr/bin/top -c -n1 -b > $LOGDIR/$DATE1/cpu_$DATE.txt
        /usr/bin/top -a -n1 -b > $LOGDIR/$DATE1/mem_$DATE.txt
        /usr/bin/mysqladmin proc stat > $LOGDIR/$DATE2/sql_$DATE.txt
        /etc/init.d/httpd fullstatus > $LOGDIR/$DATE2/apache_$DATE.txt
        ipcs -a > $LOGDIR/$DATE2/ipcs_$DATE.txt

fi
