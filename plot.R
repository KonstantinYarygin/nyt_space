setwd('/home/konstantin/documents/projects/nyt_space/')
rm(list=ls())
dev.off()

df <- read.csv('nasa_counts.csv', header=F)
colnames(df) <- c('year', 'n_all', 'n_nasa')
df$n_not_nasa <- df$n_all - df$n_nasa
df <- df[order(df$year), ]
rownames(df) <- df$year
head(df)

pdf('NASA_mentions.pdf', 9, 6)
counts <- table(df$year, df$n_nasa, df$n_not_nasa)
barplot(t(as.matrix(df[, c('n_nasa', 'n_not_nasa')])),
        axes=F, col=c('gray40', 'gray70'))
axis(side=2, labels=seq(0, 500, 100), at=seq(0, 500, 100), lwd=2, las=1)

legend('topleft', c('NASA not mentioned', 'NASA mentioned'),
       col=c('gray70', 'gray40'),
       pch=15, pt.cex=1, # points param
       bty='n')
dev.off()
