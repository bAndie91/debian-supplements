
.PHONY: network-manager-dnsmasq
network-manager-dnsmasq: /etc/NetworkManager/dnsmasq.d/cache
	crudini --set /etc/NetworkManager/NetworkManager.conf main dns dnsmasq
	service network-manager restart

/etc/NetworkManager/dnsmasq.d/cache: cache
	install $< $@

.PHONY: custom-dnsmasq-cache
all: /etc/resolv.conf /etc/resolv.conf.dnsmasq /etc/dnsmasq.conf

/etc/resolv.conf.dnsmasq: resolv.conf.dnsmasq
	install $< $@

/etc/dnsmasq.conf: dnsmasq.conf
	install $< $@
	service dnsmasq restart

/etc/resolv.conf: resolv.conf
	install $< $@
