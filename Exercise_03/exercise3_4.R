library(package = "lattice");

data <- read.table("E:/Dropbox/University_Bonn/Summer_Semester_2016/Network\ Security/Exercise_03/exercise3_4_counters.txt", header = TRUE);
attach(data);

# print (bits)
# print (times)

# xyplot(times ~ bits, xlab="Bits", ylab="Timess", type="b", lwd="2", data=data)


plot(bits, times, ylim = c(0, 1200000), type="b", lwd="2")
text(bits, times, labels=round(times,2),pos=3)
