---
layout: post
title:  "Setting up a computational cluster (HPC), part 1"
date:   2015-06-11
categories: computer chemistry
---

So by the power elimination I got put in charge of administration/setup of the local cluster system for the theoretical/computational chemistry department. The current system was completely out-dated, and made it impossible to apt-get update/upgrade, so with the addition of additional 60+ nodes from another cluster it was up to me to save the system! Which practically means I had to set it up from scratch. And a lot of googling. So much googling.

So here is what I did.

First thing first, I wanted it easily maintainable and scalable. There is no way I wanted to install software manually on all the nodes, which means all installation and setup needs to be done automatically from the masternode (frontend).

This was done via PXE/TFTP booting, and installing of a netboot Debian image (with a few extra packages). After the Debian installation, package management and configuration of the nodes is done via Puppet.

To speed things up, the whole installation is done via a local apt-get mirror on the master node. This also insures that all the packages are exactly the same version.

What you need of physical hardware:

- a frontend computer (192.168.10.1) (probably with two ethernet ports)
- Nx nodes (192.168.10.x)
- switch(s)
- Ethernet cables

The frontend:

- hosts a apt-mirror
- hosts all the user accounts (NIS/ypbind)
- hosts home folder (for NFS)
- running {DHCP, TFTP, DNS} (via DNSMASQ) and has PXE image
- running Puppetmaster
- running apache
- running slurm

the nodes:

- uses the frontend for apt-get server
- uses frontend NIS for all user accounts
- network mounted home folder (NFS)
- running puppet agent
- running slurm deamon

## Setup of the master

### Setup apt-mirror

We want all the nodes to have the same packages installed, also on the frontend, for consistency. The way this is implemented is to have local copy of the apt-get server. You will need apache for http requests.

    apt-get install apt-mirror
    mkdir /srv/apt # basepath
    vi /etc/apt/mirror.list # edit and set basepath in

Remember to add debian-installer to the repository list, or the netboot (later on) will have trouble installing debian. Your mirror list should look something like this;

    /etc/apt/mirror.list

    set base_path    /srv/apt
    set nthreads     20
    set _tilde       0

    deb http://ftp.dk.debian.org/debian/ jessie main main/debian-installer
    deb-src http://ftp.dk.debian.org/debian/ jessie main

After configuration, apt-mirror and create a symbolic link in your apache webfolder. Apt-mirror will take a few hours to download (approximate 70-90gb)

    apt-mirror
    cd /var/www
    sudo ln -s /srv/apt/mirror/ftp.dk.debian.org/debian debian # create symbolic link to the mirror

Now we edit our source list to point and our own mirror instead of the internet

    /etc/apt/source.list

    deb http://192.168.10.1/debian/ jessie main

so we know that we are using same packages as the nodes. Now to update our system we need too;

**on the frontend**

    apt-mirror
    apt-update
    apt-upgrade

**on the nodes**

    apt-update
    apt-upgrade

## Setup DHCP, DNS and TFTP with DNSMASQ

The first thing to setup is the DHCP server on the frontend, and because we want to run a DNS server as well, the easiest service to setup is dnsmasq, instead of ics-dhcp etc.

    apt-get install dnsmasq

after installation we configure the server with /etc/dnsmasq.conf.

We want to serve DHCP on eth0 interface with TFTP/PXE boot in range 192.168.10.x. For all nodes the mac addresses are then registered

    /etc/dnsmasq.conf

    interface=eth0
    dhcp-range=192.168.10.10,192.168.10.255,72h
    # tftp boot
    dhcp-boot=pxelinux.0,pxeserver,192.168.10.1
    pxe-service=x86PC, "Install Debian", pxelinux
    enable-tftp
    tftp-root=/srv/tftp
    # log
    log-queries
    log-dhcp
    log-facility=/var/log/dnsmasq
    # nodes
    dhcp-host=00:33:64:b1:83:94,node-hostname

We server internet on eth1 and local dhcp on eth0, so we setup a static ip on eth0

    /etc/network/interface

    auto eth0
    iface eth0 inet static
    address 192.168.10.1
    netmask 255.255.255.0

Notice the dhcp-host line where I couple a mac-address to a hostname. The same hostname is then added to the /etc/hosts, for example;

    192.168.10.23   node-hostname

## Setup PXE booting image

download netboot/netboot.tar.gz for the version of Debian you are using, and setup the PXE boot;

    mkdir /srv/tftp
    cd /srv/tftp
    tar -xf netboot.tar.gz
    vi pxelinux.cfg/default

edit and setup PXE to use a preseed configuration. If you are unsure what to
put in your preseed script, you can always manually install debian and check
the debconf-get-selections --installer > preseed.cfg output after the
installation, or look at this guide (https://www.debian.org/releases/stable/amd64/apbs04.html.en)[https://www.debian.org/releases/stable/amd64/apbs04.html.en]

    pxelinux.cfg/default

    default install
    label install
        menu label ^Install
        menu default
        kernel debian-installer/amd64/linux
        append initrd=debian-installer/amd64/initrd.gz auto=true priority=critical url=http://192.168.

The preseed cfg is placed in the apache http folder so it can be loaded over the net. Remember to setup the mirror settings to use the local mirror on the frontend.

    /var/www/sunray-preseed.cfg

- https://github.com/charnley/debian-cluster-configuration/blob/master/var/www/sunray-preseed.cfg

## Setup NIS and NFS

Next is setup of user management and network shared folders (home and opt).

    apt-get install nfs-common nfs-kernel-server

Set the mount drives

    /etc/exports

    /home 192.168.10.1/255.255.255.0(rw,sync,no_subtree_check)
    /opt 192.168.10.1/255.255.255.0(rw,sync,no_subtree_check)

and run

    nfs-kernel-server restart
    showmount -e

And now for NIS

    apt-get install nis

give it a NIS domain (remember it, mine was "sunray-nis")

Setup the master to be the server, by editing the file `/etc/defaults/nis` making sure that you have the following lines:

    NISSERVER=true
    NISCLIENT=false

Once this is done you need to control which machines are allowed to access the NIS server.
Do this by editing the file `/etc/ypserv.securenets` as in the following example:

    # Restrict to 192.168.1.x
    255.255.255.0 192.168.1.0

Run the configuration for NIS

    /usr/lib/yp/ypinit -m

and restart nis

    service nis restart

Next "setting up puppet/nodes"...
