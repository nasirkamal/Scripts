user=cbt
password=Dell0SS!

adduser $user
echo $password | passwd $user --stdin
echo "$user ALL=(root) NOPASSWD:ALL" >> /etc/sudoers.d/$user
chmod 0400 /etc/sudoers.d/$user
