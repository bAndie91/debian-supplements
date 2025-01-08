
.PHONY: default
default:
	false


.PHONY: install-on-network-manager-based-system
install-on-network-manager-based-system: config-network-manager ensure-resolvconf ensure-unbound config-unbound

.PHONY: config-network-manager
config-network-manager:
	crudini --set /etc/NetworkManager/NetworkManager.conf main dns default
	crudini --set /etc/NetworkManager/NetworkManager.conf main rc-manager resolvconf
	service network-manager restart

.PHONY: ensure-resolvconf
ensure-resolvconf:
	resolvconf --updates-are-enabled

.PHONY: ensure-unbound
ensure-unbound:
	unbound-control status

.PHONY: config-unbound
config-unbound: /etc/default/unbound.d/resolvconf-update /etc/unbound/unbound.conf.d/upstream.conf /etc/unbound/unbound.conf.d/private-reverse-zones.conf
	service unbound restart

/etc/default/unbound.d/resolvconf-update: resolvconf-update
	cp $< $@

/etc/unbound/unbound.conf.d/upstream.conf: upstream.conf
	cp $< $@

/etc/unbound/unbound.conf.d/private-reverse-zones.conf: private-reverse-zones.conf
	cp $< $@


.PHONY: custom-dnsmasq-cache
custom-dnsmasq-cache: /etc/resolv.conf /etc/resolv.conf.dnsmasq /etc/dnsmasq.conf

/etc/resolv.conf: resolv.conf
	cp $< $@

/etc/resolv.conf.dnsmasq: resolv.conf.dnsmasq
	cp $< $@

/etc/dnsmasq.conf: dnsmasq.conf
	cp $< $@
	service dnsmasq restart
