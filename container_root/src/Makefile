_rpm_build := /build/rpmbuild

.PHONY: all
all:
	mkdir -p $(_rpm_build)
	for dir in RPMS SOURCES SPECS SRPMS BUILD; do \
	    mkdir -p $(_rpm_build)/$$dir; \
	done
	echo '%_topdir %(echo $$HOME)/rpmbuild' > /build/.rpmmacros
	cp /src/3pp/*.tar.?z $(_rpm_build)/SOURCES
	cp /src/rush.spec $(_rpm_build)/SPECS
	rpmbuild -ba $(_rpm_build)/SPECS/rush.spec --nodebuginfo
	cp $(_rpm_build)/SRPMS/*.src.rpm /dist
	cp $(_rpm_build)/RPMS/x86_64/*.rpm /dist
