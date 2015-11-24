args <- commandArgs(trailingOnly = TRUE)
load("predictMorphRelWorkspace.RData")
t <- read.delim(args[1],header=F)

t$V3 <- as.numeric(as.character(t$V3))
t$V4 <- as.numeric(as.character(t$V4))
t$V5 <- as.numeric(as.character(t$V5))

t[t$V5 <= 0,]$V5 <- 0.00001

t$V3 <- (t$V3 - mean_spell) / sd_spell
t$V4 <- (t$V4 - mean_trans) / sd_trans
t$V5 <- (log(t$V5) - mean_sem) / sd_sem 

t[,c('key_word1_pca1','key_word1_pca2')] <- do_pca(t$V3,t$V4,t$V5)
t$key_word2_pca1 <- average_unrelated_pca1
t$key_word2_pca2 <- average_unrelated_pca2

t$P <- predict(best_model,t, type='response')
alts <- t[t$P >= 0.84,]
nrow(alts)
if (nrow(alts) > 0){
  filename = as.character(sample.int(10000000,1))
  write.table(alts,file=paste('blah/',filename,'.txt',sep=''),append=T,quote=F,sep='\t',row.names=F,col.names=F)
}