#!/usr/bin/perl
use FindBin qw($Bin);

die "perl $0 <Chr> <Len> <Wild> <Cult> <window> \n" if($#ARGV<3);
my $chr=shift;
my $len=shift;
my $wild=shift;
my $cult=shift;
my $loci=shift;
my $window=shift;

$window ||=50000;
my $bin=$window*0.1;
$loci ||=0;

my $out="$cult\_$wild";
mkdir  "$out" unless (-d $out);
my $pwd=`pwd`;
chomp $pwd;
system "cd $out";
my $file="$pwd/$out/$chr.geno";
my $output="$pwd/$out/$chr.fst.single";
my $output_overall="$pwd/$out/$chr.fst.overall";
`rm $output `if (-f $output);
`rm $output_overall` if(-f $output_overall);
my $R="$pwd/$out/$chr.R";

open R,">$R" or die  "$!";
print R "library(\"hierfstat\")\n";		#install hierfstat and ade4 through root 
#print R "library(\"hierfstat\", lib.loc=\"/home/lint\")\n";
print R "read.table(\"$file\")->aa\n";
print R "basic.stats(aa)->output\n";
print R "write.table(output\$perloc,\"$output\",append=T,col.names=F)\n";
print R "write.table(output\$overall,\"$output_overall\",append=T,col.names=F)\n";
print R "q()\n";
open OUT,">$output" or die "$!";
print OUT "Loci Ho Hs Ht Dst Htp Dstp Fst Fstp Fis Dest\n";
close OUT;
my $geno="$pwd/$out/$chr.genotype";
my $genotype="/public/cau/lintao_group/chenke/tao_lab/Brassica_oleracea/03_Selection/00_rawdata/Clade1_vs_Clade4/$chr.final.genotype";
for(my $i=0;$i<$len;$i+=$bin){
     next if($i<$loci);
     my $st=$i;
     my $en=$i+$window;
    `cat $genotype |awk '\$2>$st && \$2<$en' >$geno`;
     #system "perl $Bin/change_genotype_fst_popu.pl $geno $file $cult $wild";
     system "perl $Bin/change_genotype_format_hierfstat.pl $geno $file $cult $wild";
     open OUT,">>$output_overall" or die  "$!";
     print OUT "$i\n";
     close OUT;
     system "/public/cau/lintao_group/lintao/software/R-3.6.0/bin/R < $R --vanilla";
#     exit;
}
