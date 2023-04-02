FROM docker.io/library/almalinux:9-minimal

RUN microdnf install -y \
	rpm-build \
	gcc \
	procps-ng \
    && microdnf clean all \
    && rm -rf /var/cache/yum

RUN useradd -ms /bin/bash -d /build build
USER build
