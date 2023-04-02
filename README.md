README.md
=========


### Build RPM ###

First you need to fetch 3PPs in the 3pp directory.
This is not required if you go for the automatic approach since the tool will
do it for you.


#### Build on the host ####

Building the rpms should only require a make.

    $ make


#### Build in a container ####

Fix SELinux label on hostpath volumes. It doesn't seem like "podman kube" can
relabel on the fly like "podman create" does.

    $ chcon -t container_file_t -l s0:c42 -R .

Or if you want to build it in a container:

    $ podman kube play --network none --userns keep-id:uid=1000 kube.yaml
    $ podman attach <container-id>

    If the was any issues:
    $ podman logs --follow <container-id>

Close down the Pod.

    $ podman kube down kube.yaml


#### Semi automatic build ####

This require an external tool from git@github.com:johro81/tool.git

    $ build_rpm .


### Build a new version of the software ###

You will have to update the following files:

* 3pp/files
* rush.spec

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
        -v .:/src:ro,Z \
        -v ./dist:/dist:Z \
        --userns keep-id:uid=1000 \
        --name test localhost/test /bin/sleep inf
    $ podman start test
    $ podman exec -it -w /src test /bin/bash

    [build@78faff19f5e0 src]$ make
    ...
    [build@78faff19f5e0 src]$ exit
    $ find ./dist

Clean up the container.

    $ podman container kill test
    $ podman container rm test

Clean up of unwanted images.

    $ podman image list
    ...
    $ podman image rm fdf651c8b3dc
    $ podman image rm ..

    or if you want to clean house

    $ podman image prune --all --force


#### Tag and push container to the registry ####

Tag container and make sure to increase the tag number.

    $ podman tag localhost/test:latest registry.example.com/rush:2
    $ podman login registry.example.com
    ...
    $ podman push
