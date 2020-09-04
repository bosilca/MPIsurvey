library(ggplot2)
library(dplyr)
library(reshape2)

#change this to your directory the rest should be fine....
setwd("/Users/ejeannot/recherche/MPIsurvey/TeX")

input_csv = "./dat/Q6-simple.csv"

generate_graph <- function(input_csv = "./dat/Q7-simple.csv", 
                           output_pdf = "./ExaMPI-SC20/R-scripts/Q7.pdf"){
  
  
  #lm<- left_margin #left margin in pt
  #Tlabels <- x_text #Labels
  T <- read.csv(input_csv,header=TRUE,sep=",",check.names=FALSE)
  
#  T$X <- gsub("\\n", " ", T$X)
 names(T)[1]<-"X"
  
  #required to put overall on the top left corner
  Torder <- sort(as.vector(T$X),partial=8:9)
  
  T<- melt(T,id.var="X")
  
  T <- arrange(mutate(T,X=factor(X,levels=Torder)),X)
  
  p<- ggplot(data=T,aes(x=X,y=value,fill=variable))+
    geom_col(aes(fill = variable), width = 0.7)+
    theme(axis.text.y = element_text(size = rel(2)),
          axis.text.x = element_text(size = rel(3), angle=45, vjust = 1,hjust=1),
          axis.title = element_text(size = rel(2)),
          axis.title.x=element_blank(),
          legend.title=element_blank(),
          legend.text = element_text(size = rel(2)))+
      labs(y = "Percentage")
  
  p
  
  # save plot 
  ggsave(output_pdf,height=10,width=20)
}

generate_graph(input_csv = "./dat/Q1-simple.csv", 
               output_pdf = "./ExaMPI-SC20/R-scripts/Q1.pdf")

generate_graph(input_csv = "./dat/Q3-simple.csv", 
               output_pdf = "./ExaMPI-SC20/R-scripts/Q3.pdf")

generate_graph(input_csv = "./dat/Q6-simple.csv", 
               output_pdf = "./ExaMPI-SC20/R-scripts/Q6.pdf")

generate_graph(input_csv = "./dat/Q21-simple.csv", 
               output_pdf = "./ExaMPI-SC20/R-scripts/Q21.pdf")

generate_graph(input_csv = "./dat/Q9-simple.csv", 
               output_pdf = "./ExaMPI-SC20/R-scripts/Q9.pdf")

generate_graph(input_csv = "./dat/Q15-simple.csv", 
               output_pdf = "./ExaMPI-SC20/R-scripts/Q15.pdf")

generate_graph(input_csv = "./dat/Q23-simple.csv", 
               output_pdf = "./ExaMPI-SC20/R-scripts/Q23.pdf")

generate_graph(input_csv = "./dat/Q29-simple.csv", 
               output_pdf = "./ExaMPI-SC20/R-scripts/Q29.pdf")

generate_graph(input_csv = "./dat/Q28-simple.csv", 
               output_pdf = "./ExaMPI-SC20/R-scripts/Q28.pdf")

