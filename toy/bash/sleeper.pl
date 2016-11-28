#!/usr/bin/perl -w

use strict;

my $time = $ARGV[0] || 1;
my $exit = $ARGV[1] || 0;

sleep $time;
exit  $exit;
