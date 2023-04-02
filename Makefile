.PHONY: all
all: clean
	bin/fetch_3pp.py container_root/src/3pp
	chcon -t container_file_t -l s0:c42 -R ./container_root
	podman kube play --network none --userns keep-id:uid=1000 build.yaml
	podman logs --follow build_rush-almalinux9
	podman kube down build.yaml 2>/dev/null || /bin/true


.PHONY: clean
clean:
	podman kube down build.yaml 2>/dev/null || /bin/true
	rm -f ./container_root/dist/*


.PHONY: 3pp_clean
3pp_clean:
	rm -f ./conatiner_root/src/3pp/*
