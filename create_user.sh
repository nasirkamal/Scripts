#!/bin/sh

user=<user>
password=<passwd>

userdel $user
rm -rf /home/$user

useradd $user
echo $password | passwd $user --stdin
echo "$user ALL=(root) NOPASSWD:ALL" >> /etc/sudoers.d/$user
chmod 0400 /etc/sudoers.d/$user
