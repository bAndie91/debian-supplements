
.PHONY: default
default:
	false


.PHONY: on-network-manager-based-system
on-network-manager-based-system: ensure-resolvconf ensure-unbound /etc/default/unbound /etc/unbound/unbound.conf.d/cache.conf /etc/unbound/unbound.conf.d/upstream.conf /etc/cron.d/unbound-persist-cache
	crudini --set /etc/NetworkManager/NetworkManager.conf main dns default
	crudini --set /etc/NetworkManager/NetworkManager.conf main rc-manager resolvconf
	service unbound restart
	service network-manager restart

.PHONY: ensure-resolvconf
ensure-resolvconf:
	resolvconf --updates-are-enabled

.PHONY: ensure-unbound
ensure-unbound:
	unbound-control status

/etc/default/unbound: unbound-start-hook
	cp $< $@

/etc/unbound/unbound.conf.d/cache.conf: cache.conf
	cp $< $@

/etc/unbound/unbound.conf.d/upstream.conf: upstream.conf
	cp $< $@

/etc/cron.d/unbound-persist-cache: unbound-persist-cache.cron
	cp $< $@


.PHONY: custom-dnsmasq-cache
custom-dnsmasq-cache: /etc/resolv.conf /etc/resolv.conf.dnsmasq /etc/dnsmasq.conf

/etc/resolv.conf.dnsmasq: resolv.conf.dnsmasq
	cp $< $@

/etc/dnsmasq.conf: dnsmasq.conf
	cp $< $@
	service dnsmasq restart

/etc/resolv.conf: resolv.conf
	cp $< $@
