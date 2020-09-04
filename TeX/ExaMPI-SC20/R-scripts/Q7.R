library(ggplot2)
library(dplyr)
library(reshape2)


# 4 lines to customize plot
setwd("/Users/ejeannot/recherche/MPIsurvey/TeX")
lm<- 35 #left margin in pt
Tlabels <- c("X","Num-App/Lib", "Lang","OS/R","Tool","Big data","Visulization","AI","Worlflow","Image Proc","Other") #Labels
T <- read.table("./dat/Q7-simple.csv",header=TRUE,sep=",")

T$X <- gsub("\\n", " ", T$X)
names(T)<-Tlabels

#required to put overall on the top left corner
Torder <- sort(as.vector(T$X),partial=8:9)

T<- melt(T,id.var="X")

T <- arrange(mutate(T,X=factor(X,levels=Torder)),X)

p<- ggplot(data=T,aes(x=variable,y=value,fill=X))+
    geom_bar(stat = 'identity', position = 'dodge')+
  theme(legend.position = "none",
        axis.text.y = element_text(size = rel(2)),
        axis.text.x = element_text(size = rel(2), angle=45, vjust = 1,hjust=1),
        axis.title = element_text(size = rel(2)),
        strip.text.x = element_text(size = rel(1)),
        axis.title.x=element_blank(),
        axis.title.y=element_blank(),
        plot.margin=unit(c(0,0,0,lm),"pt"))+
  facet_wrap(~X)

p

# save plot 
ggsave("./ExaMPI-SC20/R-scripts/Q7.pdf")
