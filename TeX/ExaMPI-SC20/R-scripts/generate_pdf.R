library(ggplot2)
library(dplyr)
library(reshape2)

#change this to your directory the rest should be fine....
setwd("/Users/ejeannot/recherche/MPIsurvey/TeX")

generate_graph <- function(input_csv = "./dat/Q7-simple.csv", 
                           output_pdf = "./ExaMPI-SC20/R-scripts/Q7.pdf", 
                           x_text = c("X","Num-App/Lib", "Lang","OS/R","Tool","Big data","Visulization","AI","Worlflow","Image Proc","Other"),
                           left_margin = 1){

  
  lm<- left_margin #left margin in pt
  Tlabels <- x_text #Labels
  T <- read.table(input_csv,header=TRUE,sep=",")

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
        axis.text.x = element_text(size = rel(3), angle=45, vjust = 1,hjust=1),
        axis.title = element_text(size = rel(2)),
        strip.text.x = element_text(size = rel(3)),
        axis.title.x=element_blank(),
        axis.title.y=element_blank(),
        plot.margin=unit(c(0,0,0,lm),"pt"))+
      facet_wrap(~X)



  # save plot 
  ggsave(output_pdf,height=10,width=20)
}

generate_graph(input_csv = "./dat/Q7-simple.csv", 
               output_pdf = "./ExaMPI-SC20/R-scripts/Q7.pdf", 
               x_text = c("X","Num-App/Lib", "Lang","OS/R","Tool","Big data","Visulization","AI","Worlflow","Image Proc","Other"),
               left_margin=60)


generate_graph(input_csv = "./dat/Q17-simple.csv", 
               output_pdf = "./ExaMPI-SC20/R-scripts/Q17.pdf", 
               x_text = c("X", "Collectives" ,"Point-to-point", "Datatypes","with OpenMP","Communicator", "One-sided", "PMPI","Persistent", "Dyn. process", "other"),
               left_margin=30)

generate_graph(input_csv = "./dat/Q27-simple.csv", 
               output_pdf = "./ExaMPI-SC20/R-scripts/Q27.pdf", 
               x_text = c("X", "No","Dyn. process", "Topologies","One-sided" ,"Error","Communicator","Datatypes","Collectives","other"))

generate_graph(input_csv = "./dat/Q18-simple.csv", 
               output_pdf = "./ExaMPI-SC20/R-scripts/Q18.pdf", 
               x_text = c("X", "SINGLE","FUNNELED", "SERIALIZED", "MULTIPLE", "Never used", "No idea"))


generate_graph(input_csv = "./dat/Q12-simple.csv", 
               output_pdf = "./ExaMPI-SC20/R-scripts/Q12.pdf", 
               x_text = c("X", "OMPI", "Intel", "MPICH",  "MVA", "Cray", "IBM", "Fujitsu", "MS", "HPE", "NEC", "No Idea", "MPC", "Sunway", "Tianhe", "other"))


generate_graph(input_csv = "./dat/Q10-simple.csv", 
               output_pdf = "./ExaMPI-SC20/R-scripts/Q10.pdf", 
               x_text = c("X", "Internet", "Other lec.",  "Standard", "School", "Books", "Never learned",  "other"))



generate_graph(input_csv = "./dat/Q14-simple.csv", 
               output_pdf = "./ExaMPI-SC20/R-scripts/Q14.pdf", 
               x_text = c("X", "Online docs", "Internet", "MPI standard", "Colleagues", "Books", "I know all", "other"),
               left_margin=30)


generate_graph(input_csv = "./dat/Q19-simple.csv", 
               output_pdf = "./ExaMPI-SC20/R-scripts/Q19.pdf", 
               x_text = c("X", "No obstacles", "Too many routines", "Complicated", "No appropriate one", "Nobody to ask", "Dislike API", "other"),
               left_margin=44)


generate_graph(input_csv = "./dat/Q22-simple.csv", 
               output_pdf = "./ExaMPI-SC20/R-scripts/Q22.pdf", 
               x_text = c("X", "OMP", "CUDA", "No", "Pthread", "OACC", "OCL", "other"))


generate_graph(input_csv = "./dat/Q24-simple.csv", 
               output_pdf = "./ExaMPI-SC20/R-scripts/Q24.pdf", 
               x_text = c("X", "No investigation",  "Framework", "PGAS", "DSL", "LL comm", "other"),
               left_margin=60)






