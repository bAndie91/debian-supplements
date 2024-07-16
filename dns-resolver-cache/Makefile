
.PHONY: all
all: /etc/resolv.conf.dnsmasq /etc/dnsmasq.conf /etc/NetworkManager/dispatcher.d/resolv-conf-domain

/etc/resolv.conf.dnsmasq: resolv.conf.dnsmasq
	install $< $@

/etc/dnsmasq.conf: dnsmasq.conf
	install $< $@
	service dnsmasq restart

/etc/NetworkManager/dispatcher.d/resolv-conf-domain: resolv-conf-domain
	install $< $@
