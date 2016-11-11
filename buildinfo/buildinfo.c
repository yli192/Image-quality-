/**
 * @file buildinfo.c
 *
 * @brief Version and build information for test
 *
 * This file was generated automatically by buildinfo.sh from your Makefile.
 * It contains the declaration of a global instance of the _buildinfo struct for
 * test. This file needs to be linked into your application or library.
 * If you are using the MIP generic Makefile then it will be automatically added
 * to the link dependencies for you.
 *
 * The name of the global struct is test_buildinfo and was derived by taking
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
 * @code Created by buildinfo.sh $Id$ @endcode
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
	
BuildInfo test_buildinfo = 
{
    "test",
    "1.0.0",
    "Wed Sep 21 12:55:39 AM EDT 2016",
    "",
    "/Users/Gary/Desktop/iqTools/buildinfo",
    "Gary",
    "Yes-MacBook-Pro.local",
    "Unversioned directory",
    "15.5.0",
    "x86_64",
    "gcc",
    "4.2.1"
};

