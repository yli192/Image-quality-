#
# Makefile for buldinfo.sh
#

PREFIX := /mip
BINDIR := $(PREFIX)/bin
INCDIR := $(PREFIX)/include/mip

all :
	@echo -e "Building test program...\n"
	./buildinfo.sh test 1.0.0 gcc
	gcc main.c buildinfo.c -o buildtest

clean :
	rm -f buildinfo.c buildtest *.o *~

install :
	@echo -e "Installing buildinfo.sh and buildinfo.h...\n"
	/usr/bin/install -d -m 755 $(INCDIR)
	/usr/bin/install -m 644 buildinfo.h $(INCDIR)
	/usr/bin/install -m 755 buildinfo.sh $(BINDIR)
