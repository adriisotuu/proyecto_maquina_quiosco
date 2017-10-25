#!/bin/sh

cat /usr/lib/systemd/system/getty@.service | grep "autologin quiosco"

if [ $? -eq 1  ] ; then
        cp /root/getty_con_autologin.conf /usr/lib/systemd/system/getty@.service
fi
