#! /bin/bash

# This script is used to create buildinfo.c at build time for
# MIP projects.  All libraries and applications should use it in their
# Makefiles. The generic mip Makefile already does this.
#
# $Id$

if [ $# -ne 3 ]; then
	echo -e "Usage: $0 <package name> <package version> <compiler>\n"
	exit -1;
fi

PACKAGE_NAME=$1
PACKAGE_VERSION=$2
COMPILER=$3

if [ "$COMPILER" = "gcc" -o "$COMPILER" = "g++" ]; then
    COMPILER_VERSION=`$COMPILER -dumpversion`
else
    COMPILER_VERSION='unknown'
fi

BUILD_INFO_NAME=`echo $PACKAGE_NAME | grep -o -E '[^ ]+$' | sed -e 's/-/_/g'`
BUILD_INFO_NAME=${BUILD_INFO_NAME}_buildinfo
BUILD_URL=`svn info | grep URL`
BUILD_DIR=`pwd`
BUILD_DATE=`date +'%a %b %e %r %Z %Y'`
BUILD_USER=$USER
BUILD_HOST="`hostname`"
BUILD_REVISION="`svnversion -n $BUILD_DIR`"
BUILD_KERNEL=`uname -r`
BUILD_MACHINE=`uname -m`

echo "---------------------------------------------------------------------"
echo "Creating buildinfo.c: $BUILD_INFO_NAME Rev: $BUILD_REVISION"
echo "---------------------------------------------------------------------"

cat > buildinfo.c  <<EOF
/**
 * @file buildinfo.c
 *
 * @brief Version and build information for $PACKAGE_NAME
 *
 * This file was generated automatically by buildinfo.sh from your Makefile.
 * It contains the declaration of a global instance of the _buildinfo struct for
 * $PACKAGE_NAME. This file needs to be linked into your application or library.
 * If you are using the MIP generic Makefile then it will be automatically added
 * to the link dependencies for you.
 *
 * The name of the global struct is $BUILD_INFO_NAME and was derived by taking
 * the last word from the Makefile macro PROJECT and changing any '-' to '_'
 * where necessary.
 *
 * You should insure that the PACKAGE and VERSION macros in your Makefile are
 * correct.
 *
 * You must also include buildinfo.h in the source file that will use the
 * buildinfo query functions. It contains static definitions of the access
 * functions.
 * 
 * @sa buildinfo.h
 *
 * @code Created by buildinfo.sh \$Id$ @endcode
 */

typedef struct _buildinfo {
    const char *package_name;
    const char *package_version;
    const char *date;
    const char *url;
    const char *dir;
    const char *user;
    const char *host;
    const char *revision;
    const char *kernel;
    const char *machine;
    const char *compiler;
    const char *compiler_version;
} BuildInfo;
	
BuildInfo $BUILD_INFO_NAME = 
{
    "$PACKAGE_NAME",
    "$PACKAGE_VERSION",
    "$BUILD_DATE",
    "$BUILD_URL",
    "$BUILD_DIR",
    "$BUILD_USER",
    "$BUILD_HOST",
    "$BUILD_REVISION",
    "$BUILD_KERNEL",
    "$BUILD_MACHINE",
    "$COMPILER",
    "$COMPILER_VERSION"
};

EOF
