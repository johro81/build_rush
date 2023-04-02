_rpm_build := ${HOME}/rpmbuild

.PHONY: all
all:
	mkdir -p $(_rpm_build)
	for dir in RPMS SOURCES SPECS SRPMS BUILD; do \
	    mkdir -p $(_rpm_build)/$$dir; \
	done
	echo '%_topdir %(echo $$HOME)/rpmbuild' > $$HOME/.rpmmacros
	cp 3pp/*.tar.?z $(_rpm_build)/SOURCES
	cp rush.spec $(_rpm_build)/SPECS
	rpmbuild -ba $(_rpm_build)/SPECS/rush.spec --nodebuginfo
	cp -rv $(_rpm_build)/SRPMS /dist/
	cp -rv $(_rpm_build)/RPMS /dist/
