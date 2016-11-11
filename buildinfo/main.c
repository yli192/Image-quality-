/*
 Test program for buildinfo.sh

 build it with:

 buildinfo.sh test 1.0.0 gcc
 gcc main.c buildinfo.c -o buildtest

*/

#include "buildinfo.h"

extern BuildInfo test_buildinfo;

int main(int argc, char **argv)
{
 char str[255];

 printf("%s\n", GetBuildSummary(&test_buildinfo));
 printf("%s\n\n", GetBuildString(&test_buildinfo));

 if (argc == 4)
 {
   if (CheckBuildVersion(&test_buildinfo, atoi(argv[1]),atoi(argv[2]),atoi(argv[3])))
     printf("%s is >= than version %s.%s.%s\n", argv[0], argv[1], argv[2], argv[3]);
   else
     printf("%s is < than version %s.%s.%s\n", argv[0], argv[1], argv[2], argv[3]);
 }
 else
   printf("Usage: %s major minor patch\n", argv[0]);
 return 0;
}
