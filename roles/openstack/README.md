Role Name
=========

Role to prepare your Virtual Machines on Openstack. Initially this playbook's only role is to mount already attached volumes to each instance as listed in inventory. This should probably expand over time.

Requirements
------------
Volumes should be attached to each of the instances.

Role Variables
--------------


Dependencies
------------


Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: servers
      become: yes
      become_method: sudo
      role: openstack

License
-------

BSD

