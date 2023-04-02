README.md
=========


### Build RPM ###

Building the rpms should only require a few simple commands:

    $ podman build --tag build -f Dockerfile
    $ make
    ...
    $ ls -l ./dist/


### Build a new version of the software ###

You will have to update the following files:

* container_root/src/3pp/files
* container_root/src/rush.spec

And hopefully this will be enough. You will have to create a new build image
if the build requirements have change and the build starts to fail.


### Update build image ###

You will have to update the following files:

* Dockerfile
* build.yaml


#### Build the image ####

Update the dockerfile and create the image with podman or buildah.

    $ podman build --tag test -f Dockerfile


#### Test out the container ####

Create and test out the container.

    $ podman create \
        -v ./container_root/src:/src:ro,Z \
        -v ./container_root/dist:/dist:Z \
        --userns keep-id:uid=1000 \
        --name test localhost/test /bin/sleep inf

    $ podman start test
    $ podman exec -it test /bin/bash

    [build@78faff19f5e0 /]$ make -f /src/Makefile
    ...

Clean up the container.

    $ podman container kill test
    $ podman container rm test

Clean up of unwanted images:

    $ podman image list
    ...
    $ podman image rm fdf651c8b3dc
    $ podman image rm ..

    or if you want to clean house

    $ podman image prune --all --force


#### Tag and push container to the registry ####

Tag container and make sure to increase the tag number

    $ podman tag localhost/test:latest registry.example.com/rush:2
    $ podman login registry.example.com
    ...
    $ podman push


### SELinux ###

SELinux can be problematic at times, these are some fixes that might be
required for mounting if host volumes to work.

Check first if you really need these:

    $ sudo setsebool -P virt_use_nfs 1
    $ sudo setsebool -P use_nfs_home_dirs 1

These should be safe to run. Podman will relabel files if you use the Z flag
with volumes.

    $ chcon -t user_home_t -l s0 -R .
    $ chcon -t container_file_t -l s0:c42 -R ./container_root
