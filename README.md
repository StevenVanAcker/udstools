Unix domain socket tools
========================

Short descriptions
------------------
* ```udshub.py``` is a server which creates and listens to a unix socket, and forwards messages sent from one client to all others.
* ```uds2fd.py``` connects to a unix domain socket and hands the filedescriptor to a program you specify.
* ```udschatclient.py``` is a debugging tool to connect to a unix domain socket and send/receive data.

Guide
-----

This toolset can be used to set up internal networking between QEMU virtual machines without requiring
root access on the host. 

QEMU allows you to create a virtual NIC for a VM, and connect it to a socket
listening on localhost. This setup is not very secure in a multi-user environment where everyone on
localhost can then connect to your QEMU internal network.

A safer approach is to connect the virtual NIC to unix domain socket, which can be shielded from
other users through filesystem permissions.

To set this up, first start ```udshub.py```:

```
$ ./udshub.py mysocket
```

Next, start a QEMU VM through ```uds2fd.py```:

```
./uds2fd.py 99:mysocket -- kvm -k en-us -localtime -m 256 -drive file=vm.qcow,if=virtio -net socket,fd=99 -net nic,macaddr=00:11:22:33:44:55
```

This command start your QEMU VM and connects a virtual NIC with the given MAC address to filedescriptor 99, which ```uds2fd.py``` has connected to the unix domain socket ```mysocket```.
Repeat the command for another VM you wish to connect to the same internal network so both VMs can communicate.

