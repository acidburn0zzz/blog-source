Title: IPv6 at Online.net, with libvirt
Date: 2017-07-14T00:21+02:00
Author: Wxcafé
Category: tutorial
Slug: ipv6_at_online.net,with_libvirt

So, I have this server at [Online](https://online.net), a french hosting
company, part of Illiad. They do an all-around amazing job hosting servers,
their interface is great, they datacenters are top-notch, etc.

But like every other hosting company out there, IPv6 isn't yet a first-class
citizen. Oh, it's supported all right. The official way to make it work involves
not one, not two, but *three* configuration methods:

- The address must be configured statically, manually
- They use Prefix Delegation (PD), so you have to run a DHCPv6 client to get the
  prefix delegated to you
- And then you need to get a default route, and since they don't implement the
  DHCPv6 extension for this (yet?) so you have to accept SLAAC (stateless
  address autoconfiguration) Router Advertisements (RAs).

So, generally, on Linux, this is a bit of a hassle. You come and configure your
static address, the kernel accepts RAs by default so that's taken care of, and
then you configure a DHCPv6 client (they have a nice tutorial for that) and
you're good to go.

Of course, there's a catch: the title of that post says "with libvirt" and
I wouldn't have written a blog post to tell you "they have a good tutorial, just
follow it!".

So libvirt is a common interface for a bunch of virtualization technologies
(Xen, Qemu/KVM, bhyve, virtualbox, etc...). It also does a bunch of nice stuff
for you, like set up a SPLICE or a VNC server for each VM, handle the resource
management in a standardized way, all that stuff. But it also handles the
network stuff for you. Which is really nice in a way, since it sets up a bridge
for the VMs to communicate, firewall rules for forwarding and stuff, a DHCP
server for the VMs, etc. And you can configure it however you want! I can just
bridge out to the NIC, or setup a v4 NAT, or whatever. It's really nice. But
then you turn on IPv6 on your libvirt network config. And just like that, poof,
your host v6 connectivity goes down.

That's weird. Reboot, the v6 connectivity doesn't even go up! Even tho you have
an address and ... wait, the default route is gone?

Yeah, so *here's* the catch. libvirt, when it starts up and one of the
configured networks has v6 enabled, launches a Router Advertisement daemon
(radvd) and starts sending RAs to *all host interfaces*. **TO ALL OF THE HOST'S
INTERFACES!!** But it doesn't know any default route to advertise to the egress
interface, so it just sends a RA without a default route. And, of course, Linux
sees that and overwrites the old default route it received from the older RA,
cause *of course* a newer RA would have better information, *even* if it says it
has no route.

Anyway, so now there isn't an easy answer to this, so I went the cheap and
dirty route : I disabled the libvirtd service, and wrote the following into my
`/etc/network/interfaces`:

```
iface eth0 inet6 static
  address 2001:bc8:30b9:<whatever>/64
  accept_ra 2
  post-up ip6tables-restore < /etc/ip6tables.conf
  post-up sleep 30; \
    echo $(ip -6 r | grep default | cut -d ' ' -f 3) > /tmp/v6_route ; \
    systemctl start libvirtd; \
    sleep 10; \
    ip -6 r a default via $(cat /tmp/v6_route)
  pre-down ip6tables-save > /etc/ip6tables.conf
```

(yeah, I know the code block is )

So, okay. Please, consider this. Yes, this is absolutely disgusting. But it
*works*. 

Please don't hit me

Anyways if you were looking for a way to make this work, here it is.
