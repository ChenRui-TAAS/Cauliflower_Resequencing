#!/path/to/R
#this program want to use Gapit to run GWAS
#encoding = utf8
#Date:2020.3.10

library(multtest)
library(gplots)
library(LDheatmap)
library(genetics)
library(ape) # required for as.phylo
library(EMMREML)
library(compiler) #required for cmpfun
library("scatterplot3d")

source("http://www.zzlab.net/GAPIT/emma.txt")           # 
source("http://www.zzlab.net/GAPIT/gapit_functions.txt")

#setwd("/path/to/folder")
argv<-commandArgs(TRUE)
#
myY <- read.table(argv[1], head = TRUE)
#myG <- read.table("PIM_BIG_SL3.0.snp.genotype.maf.geno.gen.hmp.txt", head = FALSE)
myG <- read.table(argv[2], head = FALSE)
#myKI <- read.table("PIM_BIG_maf_geno_kinship.txt", head = FALSE)
#myCV <- read.table("PIM_BIG_population_structure.txt",head=TRUE)
myGAPIT <- GAPIT(Y=myY,G=myG,PCA.total=3)
#KI=myKI,
#CV=myCV
#)




