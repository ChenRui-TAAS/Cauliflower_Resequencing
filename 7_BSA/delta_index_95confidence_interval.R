#!usr/bin/Rscript
#2019/12/24

argv<-commandArgs(TRUE)
pdf(argv[3],20,6)
par(mar=c(5,4.5,4.5,5))
a <- read.table(argv[1],header=F)
b <- read.table(argv[2],header=F)
chr_num <- length(a[,1])
chr_len <- 0
b[,1] <- as.factor(b[,1])
for (i in 1:chr_num){
	snp <- subset(b,b$V1 == levels(b[,1])[i])
	chr_len <- c(chr_len,snp[,2][length(snp[,2])])
}
#chr_len
#plot(1,1,type="n",ylab=expression(Delta(SNP_index)),xlim=c(0,sum(chr_len)),ylim=c(-0.5,1),axes=F)
#par(new=T)
len_total <- 0
len_total_p <- 0
for (j in 1:chr_num){
	c <- subset(b,b$V1 == paste('Chr',j,sep=''))
	len_total <- len_total+chr_len[j]
	len_total_p <- c(len_total_p,len_total)
for (k in 1:length(c[,2])){
	plot(1,1,type="n",xaxs="i",yaxs="i",xlim=c(0,sum(chr_len)),ylim=c(-1,1),axes=F)
	points(len_total+c[k,2],c[k,17],type="p",pch=20,col="blue")
	points(len_total+c[k,2],c[k,14],type="p",pch=20,col="red")
	points(len_total+c[k,2],c[k,13],type="p",pch=20,col="red")
	par(new=T)
	plot(1,1,type="n",xaxs="i",yaxs="i",xlim=c(0,sum(chr_len)),ylim=c(0,2000),axes=F)
	#plot(1,1,type="p",xaxs="i",yaxs="i",xlim=c(0,sum(chr_len)),ylim=c(0,10000),axes=F,col="green")
	points(len_total+c[k,2],c[k,4],type="h",col="gray")###SNP number
	par(new=T)
	}
	par(new=T)
}
#print(len_total)
len_total_p <- c(len_total_p,sum(chr_len))
len_total_p1 <- len_total_p[2:11]
#print(len_total_p)
axis(4,at=seq(0,2000,500),labels=seq(0,2000,500),col.axis="black",lty=1,lwd=0.6)
mtext("SNP_number",side=4,line=2)
axis(2,at=seq(0,2000,500),labels=seq(-1,1,0.5),col.axis="black",lty=1,lwd=0.6)
#axis(2,pos=10000,at=seq(-1,1,0.5),labels=seq(-1,1,0.5),col.axis="black",lty=1,lwd=3)
mtext("delta_SNP_index",side=2,line=2)
axis(1,pos=0,at=c(0,len_total_p1[2]/2,len_total_p1[2]/2+len_total_p1[3]/2,len_total_p1[3]/2+len_total_p1[4]/2,len_total_p1[4]/2+len_total_p1[5]/2,len_total_p1[5]/2+len_total_p1[6]/2,len_total_p1[6]/2+len_total_p1[7]/2,len_total_p1[7]/2+len_total_p1[8]/2,len_total_p1[8]/2+len_total_p1[9]/2,len_total_p1[9]/2+len_total_p1[10]/2,len_total_p1[10]),labels=c("","Chr1","Chr2","Chr3","Chr4","Chr5","Chr6","Chr7","Chr8","Chr9",""))
mtext("Chr_name",side=1,line=2)
#plot(1,1,type="p",xaxs="i",yaxs="i",xlim=c(0,sum(chr_len)),ylim=c(0,10000),axes=F,col="green")
abline(v=c(len_total_p1[2],len_total_p1[3],len_total_p1[4],len_total_p1[5],len_total_p1[6],len_total_p1[7],len_total_p1[8],len_total_p1[9],len_total_p1[10]),lty=2,lwd=1.3)
#abline(v=c(55196197+71907788+18219247),lty=2,lwd=3,col="red")###CAL1
#abline(v=c(55196197+71907788+79842669+65683070+54220099+37914649),lty=2,lwd=3,col="red")###CAL2
#abline(v=c(55196197+71907788+79842669+65683070+54220099+48937047+10664326),lty=2,lwd=3,col="red")###AGL8
#abline(v=c(55196197+71907788+79050822),lty=2,lwd=3,col="red")###TFL1
#abline(v=c(55196197+3296877),lty=2,lwd=3,col="red")###LFY2
#abline(v=c(55196197+71907788+36304571),lty=2,lwd=3,col="red")###LFY1


dev.off()

#pdf("/public/cau/lintao_group/yangqinqin/database/cucumber/script_output/delta_index_Chr1_picture.pdf",12,5)
#par(mar=c(5,4.5,5,4.5))
#a <- read.table("/public/cau/lintao_group/yangqinqin/database/cucumber/script_output/sliding_result/Chr1_sliding.txt",sep="\t",header=F)
#chr_len <- a[,2][length(a[,2])]
#plot(a[,2],a[,4]/10000,type="h",col="gray",xlab="Chr1",ylab="SNP_index",axes=FALSE,xlim=c(0,chr_len),ylim=c(0,1))
#points(a[,2],a[,7],type="p",pch=20,col="blue")
#axis(1,at=seq(0,chr_len,100000),labels=NULL,col.axis="black",lty=1,lwd=0.6)
#axis(2,at=seq(0,1,0.2),labels=NULL,pos=0,col.axis="black",lty=1,lwd=0.6)
#axis(4,at=seq(0,1,0.2),labels=seq(0,10000,2000),pos=chr_len,col.axis="black",lty=1,lwd=0.6)
#lines(c(0,chr_len),c(0.5,0.5),col="red")
#mtext("SNP_number",side=4)
#dev.off()
