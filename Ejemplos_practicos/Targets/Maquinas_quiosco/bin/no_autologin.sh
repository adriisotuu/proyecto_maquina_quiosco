#!/bin/sh

cat /usr/lib/systemd/system/getty@.service | grep "autologin quiosco"

if [ $? -eq 0  ] ; then
	cp /root/getty_sin_autologin.conf /usr/lib/systemd/system/getty@.service
fi
