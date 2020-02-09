#!bin/bash

#Gotten from https://www.rabbitmq.com/man/rabbitmqctl.1.man.html
USER="swims"
PASS="pw4swims"
VHOST="swims_vhost"

# Assert Root User
SCRIPTUSER=`whoami`
if [ "$SCRIPTUSER" != "root" ]
then
    echo "You must be root to run this script. Try sudo?"
    exit 1
fi

#Configure
rabbitmqctl add_user $USER $PASS
rabbitmqctl set_user_tags $USER administrator
rabbitmqctl add_vhost /$VHOST
rabbitmqctl set_permissions -p /$VHOST $USER ".*" ".*" ".*"
#rabbitmqctl delete_user guest #Remove the guest user if they exist. Its just safer
service rabbitmq-server restart
