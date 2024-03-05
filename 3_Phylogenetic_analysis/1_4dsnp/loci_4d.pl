#!/usr/bin/perl
use Data::Dumper;

my $gff=shift;
my $cds=shift;


my %codons=(
		'CTT'=>'L', 'CTC'=>'L', 'CTA'=>'L', 'CTG'=>'L',
		'GTT'=>'V', 'GTC'=>'V', 'GTA'=>'V', 'GTG'=>'V',
		'TCT'=>'S', 'TCC'=>'S', 'TCA'=>'S', 'TCG'=>'S',
		'CCT'=>'P', 'CCC'=>'P', 'CCA'=>'P', 'CCG'=>'P',
		'ACT'=>'T', 'ACC'=>'T', 'ACA'=>'T', 'ACG'=>'T',
		'GCT'=>'A', 'GCC'=>'A', 'GCA'=>'A', 'GCG'=>'A',
		'CGT'=>'R', 'CGC'=>'R', 'CGA'=>'R', 'CGG'=>'R',
		'GGT'=>'G', 'GGC'=>'G', 'GGA'=>'G', 'GGG'=>'G'
	   );

open CDS,$cds  or die  "$!";
$/=">";
<CDS>;
my %cds_4d_site;

my %base;

while(<CDS>){
	chomp;
	my ($id,$seq)=split(/\n/,$_,2);
	$id=$1 if($id=~/^(\S+)/);
	$seq=~s/\s+//g;
	my $len=length $seq;
	for(my $i=0;$i<$len-3;$i+=3){
		my $codon=substr($seq,$i,3);
		if($codons{$codon}){
			my $loci=$i+3;
			push @{$cds_4d_site{$id}},$loci;
			push @{$base{$id}},substr($codon,2,1);
#			print $id,"\t",$loci,"\t$codon\n";
		}
	}
}
close CDS;
$/="\n";
#exit;
my %gff;
read_gff($gff,\%gff);

#print Dumper \%gff;

foreach my $gene(keys %gff){
	my $strand=$gff{$gene}{strand};
	my $chr=$gff{$gene}{chrome};
	next if(!exists $gff{$gene}{exon});

	my @exon = @{$gff{$gene}{exon}};
	my @cds_4d_size=@{$cds_4d_site{$gene}};
	my @base=@{$base{$gene}};

#	print  Dumper \@exon;

	if($strand eq '-'){
		my $len=$exon[-1][1]-$exon[-1][0]+1;
		my $id=$#exon-1;
		my $end=$exon[-1][1];
		my $len2=0;

		for (my $m=0;$m<=$#cds_4d_size;$m++){
                        if($cds_4d_size[$m]>$len){
				$len2=$len;
                                $len+=$exon[$id][1]-$exon[$id][0]+1;
                                $end=$exon[$id][1];
                                $id--;
                        }
			my $lo=$end-($cds_4d_size[$m]-$len2)+1;
			print "$chr\t$gene\t$lo\t$strand\t$cds_4d_size[$m]\t$base[$m]\t$len\n";
		}

	}
	if($strand eq '+'){

		my $len=$exon[0][1]-$exon[0][0]+1;
		my $start=$exon[0][0];
		my $id=1;

		my $len2=0;

		for (my $m=0;$m<=$#cds_4d_size;$m++){
			if( $cds_4d_size[$m] > $len ){	
				$len2=$len;
				$len+=$exon[$id][1]-$exon[$id][0]+1;
				$start=$exon[$id][0];
				$id++;
			}
			my $lo=$cds_4d_size[$m]-$len2+$start-1;
			print "$chr\t$gene\t$lo\t$strand\t$cds_4d_size[$m]\t$base[$m]\t$len\n";
		}
	}
}


sub read_gff{

	my $file=shift;
	my $ref=shift;

	open IN,$file or die "$!";
	while(<IN>){
		next if(/^\#/);
		s/^\s+//;
		s/\s+$//;
		my @t = split(/\t/);
		my $tname = $t[0];
		my $qname;
		if ($t[2] eq 'mRNA' || $t[2] eq 'CDS') {
			$qname = $1 if($t[8] =~ /^GenePrediction\s+(\S+)/ || $t[8] =~ /^ID=([^;]+);*/ || $t[8] =~ /^Parent=([^;]+);*/);
		}

		if ($t[2] eq 'mRNA' || $t[2] eq 'match') {
			$ref->{$qname}{strand} = $t[6];
			$ref->{$qname}{chrome} = $tname;
		}
		if ($t[2] eq 'CDS' || $t[2] eq 'HSP' || $t[2] eq 'exon') {
			push @{$ref->{$qname}{exon}}, [$t[3],$t[4]];
		}


	}
	close(IN);

##print Dumper $ref;

##change the exon order
#	foreach my $chr (keys %$ref) {
#		my $chr_p = $ref->{$chr};
	foreach my $gene (keys %$ref) {
		my $gene_p = $ref->{$gene};
		next if(!exists $gene_p->{exon});
		my @exon = sort {$a->[0] <=> $b->[0]} @{$gene_p->{exon}};
		$gene_p->{exon} = \@exon;
	}
#	}

}




