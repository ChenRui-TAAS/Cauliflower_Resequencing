#!/usr/bin/perl

my $individual=shift;
my $geno_list=shift;


my %hash;
open IA,$individual or die "$!";
while(<IA>){
	chomp;
	my @f=split;
	$hash{$f[0]}=$f[1];
}
close IA;

open IN,$geno_list or die  "$!";
my %line;
my $len;
while(<IN>){
	chomp;
	my $file=$_;
	open IA,$file or die  "$!";
	while(<IA>){
		next if(/N/);
		my @f=split;
		shift @f;
		for (my $i=1;$i<=$#f;$i++){
			$line{$i}.=$f[$i];
		}
		$len++;
	}
	close IA;
}
close IN;

open OA,">$geno_list.phylip";
my @key=keys %line;
my $sample_id=$#key+1;
print  OA "$sample_id\t$len\n";
foreach  my $k(sort {$a<=>$b} keys %line){
	my $mark="IND$k";
	print OA "$hash{$mark}\t$line{$k}\n";
}
close OA;
