
.PHONY: all
all: /etc/resolv.conf /etc/resolv.conf.dnsmasq /etc/dnsmasq.conf

/etc/resolv.conf.dnsmasq: resolv.conf.dnsmasq
	install $< $@

/etc/dnsmasq.conf: dnsmasq.conf
	install $< $@
	service dnsmasq restart

/etc/resolv.conf: resolv.conf
	install $< $@
