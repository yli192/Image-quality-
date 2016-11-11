
PROGRAMLIBS = -lmiputil -limgio 

TOPDIR  := .
SRCDIR  := ./src
HDRDIR  :=
OBJDIR  := ./obj
MANDIR  := ./man
DATADIR := ./share
INFODIR := ./info
DOCDIR  := ./docs


prefix := /mip

bindir     = $(prefix)/bin
libdir     = $(prefix)/lib64
includedir = $(prefix)/include
mandir     = $(prefix)/share/man
datadir    = $(prefix)/share
infodir    = $(prefix)/info


CXX = g++
CXXFLAGS = -g3 -O3 -Wall
CPPFLAGS = -I. -I$(SRCDIR) -I$(HDRDIR) -I$(TOPDIR) -I$(includedir) -I$(SUBDIRS)/src

LDFLAGS = -L. -L$(OBJDIR) -L$(TOPDIR) -L$(libdir) -L$(SUBDIRS)



$(CXX) $(CXXFLAGS) ./src/thresholding.cpp -o thresholding 
