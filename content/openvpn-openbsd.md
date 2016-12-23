Title: OpenVPN on OpenBSD
Date: 2016-11-30T23:59+01:00
Author: Wxcafé
Category: Tutorial
Slug: openvpn-openbsd

So this is a small article, because I wanted to see if I could write more if
I just wrote small things like that about a single, simple thing I did, without
too much detail and fluff

Also, I'm writing this in English, while I usually write in French. I'm
switching language because I believe English is a lot easier to express
technical concepts in, or at least I'm more fluent in it when it comes to
expressing technical concepts, and I believe now that my audience (at least, the
people I know/talk to on twitter/IRC/etc...) speak or read English much more
than French, and so it makes more sense for me to write in English here.
Therefore, I'll be writing in English only on this blog from now on.


(French version :)
De plus, j'écris ceci en Anglais, alors que j'écrivais ici habituellement en
Français. Je change de langue, parce qu'il me semble qu'il est plus facile
d'exprimer des concepts techniques en Anglais qu'en Français, ou en tout cas
que cela m'est plus facile personnellement, mais aussi parce que je pense que
mon audience (ou en tout cas, les gens que je connais/auxquels je parle sur
twitter/IRC/etc...), parlent ou lisent l'Anglais bien plus que le Français, et
il est donc plus logique pour moi d'écrire en Anglais ici.
J'écrirais donc uniquement en Anglais sur ce blog a partir de maintenant.

So, now that that's done, I can go on and write that "small article" I promised
at the top.

So, the idea is that I had a FreeBSD OpenVPN box that I used to have
a semi-decent Internet connection while at school (my school blocks all ports
that are not tcp/80 or tcp/443 or udp/53, basically. And apparently udp/443
too...). I wanted to try running that VM on OpenBSD, because of three things :

1. I really like OpenBSD, and wanted to have a VM that I could do some
experiments on without breaking all of my stuff,
2. I found a way to run OpenBSD on the provider I used for that box,
[vultr](https://vultr.com), and
3. why not?

Anyway, so once you've installed the OS, the first thing to do is

	::bash
	$ doas pkg_add openvpn

...

well okay the first thing to do is to

	# vi /etc/doas.conf

and put this in it :

	::bash
	permit keepenv :wheel as root
	permit nopass root as root

once this is done, you can now go and install the packages, before creating the
CA:

	$ doas pkg_add vim openvpn easy-rsa
	$ cd /usr/local/share/easy-rsa
	$ doas ./easyrsa init-pki
	$ doas ./easyrsa gen-dh
	$ doas ./easyrsa build-ca [nopass]
	$ doas ./easyrsa build-server-full [CN of the server] [nopass]
	$ doas ./easyrsa build-client-full [CN of a client] [nopass]

please note that you can use passwords on all of those, but then you'll have to
type them every time you use one of them. I see no problem with having
a password on the CA and the client, but the server should be able to restart by
itself in my opinion.

Anyway, now we can write the config for OpenVPN:

	$ doas mkdir /etc/openvpn/
	$ doas vim /etc/openvpn/openvpn.conf

We'll run with these settings :

	dev tap
	tls-server
	cert /usr/local/share/easy-rsa/pki/issued/[CN of the server].crt
	key /usr/local/share/easy-rsa/pki/private/[CN of the server].key
	ca /usr/local/share/easy-rsa/pki/ca.crt
	dh /usr/local/share/easy-rsa/pki/dh.pem
	proto udp
	port 53
	verb 3
	status /var/log/openvpn-status.log
	ifconfig 172.16.0.10 255.255.0.0
	route-gateway 172.16.0.10
	persist-key
	persist-tun
	keepalive 10 120
	server 172.16.0.0 255.255.0.0
	client-to-client
	tls-cipher TLS-DHE-RSA-WITH-AES-256-CBC-SHA TLS-DHE-RSA-WITH-CAMELLIA-256-CBC-SHA
	push "route 172.16.0.0 255.255.0.0"

Of course, feel free to edit that to match whatever you need.

Anyway, the next thing we need to do is to configure pf.

What, you thought that was it? Of course we're gonna filter this, it's an
internet-facing server!

	$ doas vim /etc/pf.conf

So, here is the pf configuration file :

	#       $OpenBSD: pf.conf,v 1.54 2014/08/23 05:49:42 deraadt Exp $
	#
	# See pf.conf(5) and /etc/examples/pf.conf

	set block-policy drop
	set skip on lo0
	block return in on ! lo0 proto tcp to port 6000:6010
	match in all scrub (no-df random-id max-mss 1440)

	block log all

	match out on egress from (tap0:network) to any nat-to (egress:0)
	pass out quick

	# ssh
	pass in on egress proto tcp from any to (egress) port 22

	# mosh
	pass in on egress proto udp from any to any port 60000:61000

	# snmp
	pass in on egress proto udp from [IP of my SNMP server] to any port 161
	pass in on egress proto udp from [IPv6 block of my SNMP server]/48 to any port 161

	# openvpn
	pass in on egress proto udp from any to (egress) port 53
	pass in on egress proto udp from any to (egress) port 443 rdr-to (egress:0) port 53
	pass in on tap0

So, this should be easy enough to read, but just in case : we skip lo, we block
X, we scrub weird packets, we block and log by default.

Then, we NAT everything that comes out of the VPN and to the 'net. We let what
comes from the server out too, tho that could be improved...

The next three blocks are easy, and then in the OpenVPN block, we let in port
udp/53, we redirect port udp/443 to udp/53, and we let everything in from the
VPN.

We have to reload pf and add a sysctl knob if we want to actually route packets
coming from the VPN:

	$ doas pfctl -f /etc/pf.conf
	$ echo 'net.inet.ip.forwarding=1' | doas tee -a /etc/sysctl.conf

And now, we simply enable the OpenVPN service, and we're done:

	$ doas rcctl enable openvpn
	$ doas rcctl enable pflogd
	$ doas rcctl start openvpn
	$ doas rcctl start pflogd
	$ doas rcctl ls on    # to check

That's it! It was actually pretty easy, I guess.

Also, if you don't know what's wrong and want to get a detailed log, run
`/usr/local/sbin/opvnpn --verb 11 --config /etc/openvpn/openvpn.conf`


Seeya!
