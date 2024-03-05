#!/usr/bin/perl
use Data::Dumper;
open IN,$ARGV[0] or die "$!";
my %id;
while(<IN>){
	chomp;
	my @aa=split(/\s+/);
	next if($aa[0] ne $ARGV[2]);
	$id{$aa[2]}=1;
	#print "$_[0]\n";
}
close IN;
open IN,$ARGV[1] or die "$!";
while(<IN>){
	chomp;
	my @aa=split(/\s+/);
	print "$_\n" if($id{$aa[1]});
}
close IN;
