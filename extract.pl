#!/usr/bin/env perl

use utf8;

my $fpath = './prefixes.txt';

open my $fh, "<:encoding(utf8)", $fpath;

my $str = "";
my $extracted = "";
my $sufflist = "";

while (<$fh>){
	$str = $_;
	($extracted) = $str =~ m/title="(.*)-"/;
	$sufflist .= $extracted;
	if($extracted) {
		$sufflist .= "\n";
		}
	}
	
close $fh;
open my $handle, ">:encoding(utf8)", "preflist.txt";
print $handle $sufflist;
close $handle;
