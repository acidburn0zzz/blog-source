Title: mastodon
Date: 2017-05-20T18:18+0200
Author: Wxcafé
Category:
Slug: mastodon

...

So. What have I been up to these last weeks, you ask (or maybe you don't care,
in which case I'm gonna tell you anyway, cause it might still be interesting to
you).

Also, why am I writing this blog post? Why, you see, I made a promise of some
kind (I'm also kinda cheating here, but whatever). I have a patreon now
([here](https://patreon.com/wxcafe)). I ask for money to fund the Mastodon
server I'm running, [here](https://social.wxcafe.net), that has almost 900 users
at the time of writing. I say *server*, but it's actually **servers**, since I'm
also hosting [this one](https://imaginair.es), less generalistic and more geared
towards creators and people who enjoy what we call "les cultures de
l'imaginaire" in french, which loosely include SF/Fantasy type settings, role
playing games, TCGs, etc. More on that one soon, but for now let's stay on
subject : why am I writing this blog post? Well, enough people were nice (or
foolish, depending on your opinion of me) enough to give me money that now
I have to keep my engagement to write a blog post a month (which means you'll
see way more posts since the last one is from... february (and I had to check)).

Anyway, yeah. That's mostly what I've been up to these last few weeks. I've
started hosting a mastodon server on social.wxcafe.net about a month back, I've
spent a while working on the mastodon codebase and issue tracker (I haven't had
time to do that as much as I'd like lately, I've been working on other project
with more urgent deadlines...), and the imaginair.es project started developing
with the help of [Ekzael](https://imaginair.es/@Ekzael) and
[Eutrapélie](https://imaginair.es/@Eutrapelie) about two and a half weeks ago.
I then worked a bit on automation and stuff (more on that soon) and the
imaginair.es mastodon instance was launched about a week and a half ago.

So, about imaginair.es. The idea with this is not to make it a single mastodon
instance, but rather to have it be a nebulæ of mastodon instances. Basically,
the main domain is to be an open discussion board, with creators and people
interested, as I said before, in SFF, etc. But then, seeing how mastodon could
be amazing for role playing, subdomains are available for, well, roleplaying
groups. Meaning you can get your own mastodon instance for your RP/RPG group,
and play online through that. I don't know about you, but I think that mastodon
would be a pretty nice medium for that. Anyway, I'm going to talk about the
technical details now so if you don't care skip the next two paragraphs.

So, how do I plan on running that many mastodon instances (ah, the rethorical
question, best friend of bloggers)? Well, that question requires a bit of
insight into how Mastodon works. First, Mastodon is comprised of three services:
web workers, a sidekiq process, and a streaming (websocket) server. Combined,
without much activity, these use up about 1 gig of RAM. I rent a [Dedibox Classic
2016](https://www.online.net/en/dedicated-server/dedibox-classic) at Online.net,
a french provider. That server has 1 Xeon (6C/12T) at 2.2Ghz and 32 Gigs of RAM.
That means that I should have enough memory to run 32 low-activity servers,
which typically RP servers should be. That would be if I did traditional
virtualization (Xen, etc), but not with KVM/Qemu, because Linux now has
a feature called KSM (Kernel Samepage Merging), that allows it to merge memory
pages that are the exact same. Meaning if I run 10 mastodon instances on that
same server, that are all copies of one another, it **should** use only 1 gig of
RAM. Of course, since users are present and different from instance to instance,
since the content they post isn't the same either, and since the system (like
all systems) isn't perfect, its not 100% efficient. But I can envision hosting
at least 100 instances on that server, for about 30€/month.

"But isn't that a security problem?" I hear you ask. Well, yes and no. Yes, it
could be a security problem, it *sounds* less secure than strictly separating
each VM and never letting them interact through the hypervisor. **But** given
the number of high-profile providers who use KVM/Qemu with KSM, I feel pretty
secure using it too, and we've seen more bugs in Xen than in KVM/Qemu (I'm talking
about KVM/Qemu specifically here, not about the kernel itself...) in recent
years. Anyway, if someone manages to get a shell on one of these and then gets
root and then uses KSM to jump between VMs and/or escape the VM entirely **AND
THEN** gets root on the host, well, I can only pray they're not pissed at me
enough to fuck with my other machines.

Anyway, so here are the projects I've been working on these last weeks. I'm
gonna continue working on these, of course, even tho I have some more pressing
projects right now, and I hope then can be useful to some people. If you'd like
to join either, feel free, of course, and if you'd like to get a private RP
instance, HMU at [@wxcafe@social.wxcafe.net](https://social.wxcafe.net/@wxcafe)

