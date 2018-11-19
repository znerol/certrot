ifeq ($(prefix),)
    prefix := /usr/local
endif
ifeq ($(exec_prefix),)
    exec_prefix := $(prefix)
endif
ifeq ($(bindir),)
    bindir := $(exec_prefix)/bin
endif
ifeq ($(datarootdir),)
    datarootdir := $(prefix)/share
endif
ifeq ($(mandir),)
    mandir := $(datarootdir)/man
endif

all: bin doc

%.1 : %.1.md
	pandoc -s -t man $< -o $@

bin:
	# empty for now

doc: \
	doc/certrot-expiry.1 \
	doc/certrot-fp.1 \
	doc/certrot-server.1

clean:
	-rm doc/certrot-expiry.1
	-rm doc/certrot-fp.1
	-rm doc/certrot-server.1
	-rm -rf dist
	-rm -rf build

install-doc: doc
	install -m 0644 -D doc/certrot-expiry.1 $(DESTDIR)$(mandir)/man1/certrot-expiry.1
	install -m 0644 -D doc/certrot-fp.1 $(DESTDIR)$(mandir)/man1/certrot-fp.1
	install -m 0644 -D doc/certrot-server.1 $(DESTDIR)$(mandir)/man1/certrot-server.1

install-bin: bin
	install -m 0755 -D bin/certrot-expiry $(DESTDIR)$(bindir)/certrot-expiry
	install -m 0755 -D bin/certrot-fp $(DESTDIR)$(bindir)/certrot-fp
	install -m 0755 -D bin/certrot-server $(DESTDIR)$(bindir)/certrot-server

install: install-bin install-doc

uninstall:
	-rm -f $(DESTDIR)$(bindir)/certrot-expiry
	-rm -f $(DESTDIR)$(bindir)/certrot-fp
	-rm -f $(DESTDIR)$(bindir)/certrot-server
	-rm -f $(DESTDIR)$(mandir)/man1/certrot-expiry.1
	-rm -f $(DESTDIR)$(mandir)/man1/certrot-fp.1
	-rm -f $(DESTDIR)$(mandir)/man1/certrot-server.1

dist-bin:
	-rm -rf build
	make DESTDIR=build prefix=/ install
	mkdir -p dist
	tar --owner=root:0 --group=root:0 -czf dist/certrot-dist.tar.gz -C build .

dist-src:
	mkdir -p dist
	git archive -o dist/certrot-src.tar.gz HEAD

dist: dist-src dist-bin

.PHONY: \
	all \
	clean \
	dist \
	dist-bin \
	dist-src \
	install \
	install-bin \
	install-doc \
	uninstall \
