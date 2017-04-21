setwd('/home/konstantin/documents/projects/nyt_space/')
rm(list=ls())
dev.off()

library(gplots)
tp_col <- function(col, alpha=0.5) {
    hex_alpha <- as.hexmode(floor(alpha * 255))
    return(paste0(col2hex(col), hex_alpha))
}

df <- read.csv('cos_sim.csv')

plot(NULL, axes=F,
     xlim=c(2003, 2016), ylim=c(0.4, 0.9),
     xlab='', ylab='Similarity', main='')
abline(v=seq(2003, 2016, 1), h=seq(0.4, 0.9, 0.05),
       col='gray80', lwd=1)
lines(similarity~year, df[df$type == 'yyu',], col='red', lwd=2, lty=1)
lines(similarity~year, df[df$type == 'yhu',], col='royalblue', lwd=2, lty=1)
lines(similarity~year, df[df$type == 'yyi',], col='green', lwd=2, lty=1)
lines(similarity~year, df[df$type == 'yhi',], col='black', lwd=2, lty=1)
axis(side=1, labels=seq(2003, 2016, 1), at=seq(2003, 2016, 1), lwd=2, las=1)
axis(side=2, labels=seq(0.4, 0.9, 0.05), at=seq(0.4, 0.9, 0.05), lwd=2, las=1)
legend('bottomright', c('year-year, union', 'year-heap, union', 'year-year, intersect', 'year-heap, intersect'),
       col=c('red', 'royalblue', 'green', 'black'),
       lwd=2,
       bty='n')
