# Certrot - Certificate monitoring utilities

A collection of scripts to monitor validity of certificates on the file system
as well as those returned by TLS servers.

[![Build Status](https://travis-ci.org/znerol/certrot.svg?branch=master)](https://travis-ci.org/znerol/certrot)

## INSTALL

*Preferred method*: Build a distribution tarball, copy it to the target machine
and unpack it there.
    
    $ make dist
    $ scp dist/certrot-dist.tar.gz me@example.com:~
    $ ssh me@example.com sudo tar -C /usr/local -xzf ~:certrot-dist.tar.gz

*Alternative method*: Check out this repository on the traget machine and
install it directly. The destination directory can be changed with the `prefix`
variable in order to change the installation prefix to something else than
`/usr/local`.

    $ make all
    $ sudo make prefix=/opt/local install

[Pandoc](https://pandoc.org) is necessary in order to build the man pages. This
step can be skipped by using the `install-bin` target.
