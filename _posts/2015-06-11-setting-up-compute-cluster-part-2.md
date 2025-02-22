---
layout: post
title:  "Setting up a computational cluster (HPC), part 2"
date:   2015-06-11
categories: computer chemistry
---

Now that we can easily provide DHCP, DNS and TFTP and a debian image for all the nodes, we want to make it easy to maintain the cluster and setup user management. For maintaining packages and configuration etc we use Puppet on Debian. So awesome!

> **NOTE:** remember to add "puppet" and "puppetmaster" in /etc/hosts on the server, so dnsmasq can provide DNS! Otherwise puppet agent will not know where to connect.

## Setup Puppet on the master

Install the puppetmaster on the master node

    apt-get install puppetmaster

A nice addition to the puppet service is the stdlib.

    puppet module install puppetlabs-stdlib

regular expression and autosign.conf for fast deployment
See the configuration of puppet here https://github.com/charnley/debian-cluster-configuration/tree/master/etc/puppet/manifests

Where NIS is setup as

    ## User Authentication
    # set NIS domain
    file {"/etc/defaultdomain": source => "puppet:///modules/nodes/defaultdomain"} ->
    # set yp server
    file {"/etc/yp.conf": source => "puppet:///modules/nodes/yp.conf"} ->
    # install NIS
    package {"nis": ensure => installed} ->
    # update passwd, shadow and gshadow
    file_line {'update passwd': path => '/etc/passwd', line => '+::::::'} ->
    file_line {'update shadow': path => '/etc/shadow', line => '+::::::::'} ->
    file_line {'update group': path => '/etc/group', line => '+:::'} ->
    file_line {'update gshadow': path => '/etc/gshadow', line => '+:::'}

Where NFS is setup as

## Network File System
    package {"nfs-common": ensure => installed}
    file_line {'nfs home':
    path => '/etc/fstab',
    line => '192.168.10.1:/home /home nfs rw,hard,intr 0 0',
    require => Package["nfs-common"],
    notify => Exec['nfs mount'],
    }
    file_line {'nfs opt':
    path => '/etc/fstab',
    line => '192.168.10.1:/opt /opt nfs rw,hard,intr 0 0',
    require => Package["nfs-common"],
    notify => Exec['nfs mount'],
    }
    exec {'nfs mount':
    command => '/bin/mount -a',
    path => '/usr/local/bin',
    refreshonly => true,
    }

You can either set `autosign.conf` in the puppet folder to just sign everything, and sign the nodes as the connect via

    puppet cert sign --all

Setup of the node
Puppet is installed via det preseed configuration by adding

    d-i pkgsel/include string openssh-server puppet facter

Puppet needs to connect and get a certificate signed by the server. This is either done by autosign or by manually signing the nodes

    puppet agent --test --waitforcert 60

Puppet is then either run by manually or by adding puppet to the `/etc/rc.local` to be run on every boot.

    /etc/rc.local

    #!/bin/bash
    echo -n "Waiting for network."
    while ! ip addr show | grep -F "inet 192.168.10" >> /dev/null
    do
        sleep 1
        echo -n "."
    done
    # Run puppet for node
    echo "Running puppet..."
    echo "boot $(date)" >> /root/puppet-node.log
    puppet agent -t | while read line; do
        echo $line
        echo $line >> /root/puppet-node.log
    done

And that's it. Happy clustering.
