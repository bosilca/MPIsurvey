library(ggplot2)
library(dplyr)
library(reshape2)

#change this to your directory the rest should be fine....
#setwd("/Users/ejeannot/recherche/MPIsurvey/TeX")
setwd("/Users/atsushi/AICS/Projects/Survey/Surveys/GIT/MPIsurvey/TeX/")

T <- read.table("dat/timeline.csv",header=TRUE,sep=",")

T$X <-as.Date(T$X,tryFormats="%Y-%m-%d")

T<- melt(T,id.var="X")
Sys.setlocale("LC_ALL", "en_GB.UTF-8")

p<- ggplot(data=T,aes(x=X,y=value,fill=variable))+
  geom_area()+
  scale_x_date(date_labels = "%b %Y", date_breaks = "1 month", 
               limits = c(min(T$X),min(T$X)+90), expand=c(0,0))+
  theme(axis.title.x=element_blank(),
        axis.title.y=element_blank(),
        legend.title=element_blank(),
        legend.position = "bottom",
        axis.text.y = element_text(size = rel(3)),
        legend.text  = element_text(size = rel(3)),
        axis.text.x = element_text(size = rel(3), angle=0, vjust =0.7,hjust=0.5),
        axis.title = element_text(size = rel(2)),
        plot.margin=unit(c(0,-70,0,0),"pt")) +
  scale_fill_brewer(palette = "Set1")


p

# save plot 
ggsave("./PARCO/Review//R-scripts/TimeSeries.pdf",height=10,width=20)
