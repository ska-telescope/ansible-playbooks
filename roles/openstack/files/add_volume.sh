#!/bin/bash
MOUNT=/mnt/data
VOLUME=/dev/vdb
PARTITION=/dev/vdb1
# create partition
echo -e "n\np\n1\n\n\nw" | fdisk $VOLUME
# format partition
mkfs.ext4 $PARTITION
# create folder
mkdir $MOUNT
# add entry to fstab
if [[ $(grep -q $MOUNT '/etc/fstab' && echo $?) ]]
then
    echo "Volume in fstab already exists."
else
    echo "$PARTITION $MOUNT auto defaults,nofail 0 3" >> /etc/fstab
    echo "New volume added"
fi
# mount the new volume without reboot
mount -a
