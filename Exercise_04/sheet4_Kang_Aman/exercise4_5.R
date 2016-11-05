data <- read.table("E:/Dropbox/PROGRAMS/Workspce_Python/NetSec/cipherSuite.txt", header = TRUE);
attach(data);

#mypath <- file.path("E:","Dropbox","PROGRAMS", "Workspce_Python", "NetSec", "exercise4_5.png")
#png(file=mypath, 1500, 900)

par(mar = c(12,12,2.75,3.5))

midpts <-barplot(data$times, main = "Cipher Suite Frequncies", ylab = "Times", 
                 ylim = c(0, 100), names.arg = "", xpd=TRUE, cex.lab=2, cex.axis=1.5)

text(x=midpts, y=-1, data$Cipher.Suite, cex=1.2, srt=40, xpd=TRUE, pos=2)
text(x=midpts, y=data$times+2, labels=as.character(data$times), cex=2, xpd=TRUE)

#dev.off()

