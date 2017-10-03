# Script for generating figure 4

library("dplyr")
library("ggplot2")
library("knitr")

# We are assuming that the working directory is the root of the project
source("R/multiplot.R")

summarized.df = readRDS( "rds-data/summarized.v2.rds" ) %>% filter( !is.na( Geom.Mean ) )

downregulated = list("FETUB", "EEGFR", "CD44", "PI16", "DPP4", "SOD3" )

# These are adapted from
# https://www.r-bloggers.com/simple-roc-plots-with-ggplot2-part-1/
# https://www.r-bloggers.com/simple-roc-plots-with-ggplot2-part-2/

rocdata <- function(grp, pred){
  # Produces x and y co-ordinates for ROC curve plot
  # Arguments: grp - labels classifying subject status
  #            pred - values of each observation
  # Output: List with 2 components:
  #         roc = data.frame with x and y co-ordinates of plot
  #         stats = data.frame containing: area under ROC curve, p value, upper and lower 95% confidence interval
  
  grp <- as.factor(grp)
  if (length(pred) != length(grp)) {
    stop("The number of classifiers must match the number of data points")
  } 
  
  if (length(levels(grp)) > 2) {
    stop("There must only be 2 values for the classifier")
  }
  
  cut <- unique(pred)
  tp <- sapply(cut, function(x) length(which(pred > x & grp == levels(grp)[2])))
  fn <- sapply(cut, function(x) length(which(pred < x & grp == levels(grp)[2])))
  fp <- sapply(cut, function(x) length(which(pred > x & grp == levels(grp)[1])))
  tn <- sapply(cut, function(x) length(which(pred < x & grp == levels(grp)[1])))
  tpr <- tp / (tp + fn)
  fpr <- fp / (fp + tn)
  roc = data.frame(x = fpr, y = tpr)
  roc <- roc[order(roc$x, roc$y),]
  
  i <- 2:nrow(roc)
  auc <- (roc$x[i] - roc$x[i - 1]) %*% (roc$y[i] + roc$y[i - 1])/2
  
  pos <- pred[grp == levels(grp)[2]]
  neg <- pred[grp == levels(grp)[1]]
  q1 <- auc/(2-auc)
  q2 <- (2*auc^2)/(1+auc)
  se.auc <- sqrt(((auc * (1 - auc)) + ((length(pos) -1)*(q1 - auc^2)) + ((length(neg) -1)*(q2 - auc^2)))/(length(pos)*length(neg)))
  ci.upper <- auc + (se.auc * 0.96)
  ci.lower <- auc - (se.auc * 0.96)
  
  se.auc.null <- sqrt((1 + length(pos) + length(neg))/(12*length(pos)*length(neg)))
  z <- (auc - 0.5)/se.auc.null
  p <- 2*pnorm(-abs(z))
  
  stats <- data.frame (auc = auc,
                       p.value = p,
                       ci.upper = ci.upper,
                       ci.lower = ci.lower
  )
  
  return (list(roc = roc, stats = stats))
}

rocplot.subsets <- function(grp, pred, subsets, p.value = FALSE){
  require(ggplot2)
  subset.names = levels( subsets )
  plotdata <- Map( function ( subset ){
    selection = subsets == subset
    selection[ is.na( selection ) ] = FALSE
    rocdata( grp[ selection ], pred[ selection ] )
  }, subset.names )
  
  annotations <- Reduce( c, Map( function ( plotdatum, subset ) {
    if (p.value == TRUE){
      annotation <- with(plotdatum$stats, paste(subset, ": AUC=",signif(auc, 2), " (P=", signif(p.value, 2), ")", sep=""))
    } else {
      annotation <- with(plotdatum$stats, paste(subset, ": AUC=",signif(auc, 2), " (95%CI ", signif(ci.upper, 2), " - ", signif(ci.lower, 2), ")", sep=""))
    }
  }, plotdata, subset.names ) )
  
  roc = Reduce( rbind.data.frame, Map( function ( plotdatum, subset ) {
    datum = plotdatum$roc
    datum$stratum = subset
    datum
  } , plotdata, subset.names ) )
  
  p <- ggplot(roc, aes( x = 1-x, y = y, colour = stratum ) ) +
    geom_line() +
    geom_abline (intercept = 1, slope = 1) +
    theme_bw() +
    scale_x_reverse("Specificity") +
    scale_y_continuous("Sensitivity") +
    scale_colour_brewer( breaks = subset.names, labels = annotations, type = "qual", palette = "Dark2" ) +
    #coord_cartesian( expand = FALSE ) +
    coord_fixed() +
    theme(
      text = element_text(size = 8),
      legend.justification=c(1,0), 
      legend.position=c(0.99,0.01),
      legend.title = element_blank()#,
      #legend.text = element_text( size = 7 )
      #legend.key = theme_blank()
    ) +
    annotate("text", x = 1, y = 0.97, label = protein, size = 5, hjust = 0)
  return(p)
}

# Make dataframe with a label corresponding to the Low Risk vs. cancer question
df.low.v.c = summarized.df %>%
  filter( Risk.category.Cancer.stage %in% c( "N/A", "Low", "Stage 1", "Stage 2", "Stage 3" ) ) %>%
  mutate( Label = Risk.category.Cancer.stage %in% c( "Stage 1", "Stage 2", "Stage 3" ) )

# Plotting code
plots <- list( )

# For each of the four proteins in figure 4
for( protein in c('CFI','PI16','CDH2','ITIH3') ){
    
    protein.df = df.low.v.c %>% filter( HGNC.Symbol == protein )
    
    # Determine up/down regulated
    upregulated = !(protein %in% downregulated)
    #plot.title = paste( protein, if (upregulated) "(upregulation)" else "(downregulation)" )
    protein.df = protein.df %>% mutate( Predictor = if (upregulated) Geom.Mean else -Geom.Mean )
    
    #print( kable( protein.df %>% group_by( Protein.Name, Label ) %>% summarize( Count = n() ) ) )
    
    #print( rocplot.single( grp = protein.df$Label, pred = protein.df$Predictor, title = plot.title ) )
    
    for.gender.df = protein.df %>% mutate( Gender = factor( Gender, c("M","F") ) ) %>% filter( !is.na( Gender ) )
    
    #print( kable( for.gender.df %>% group_by( Protein.Name, Label, Gender ) %>% summarize( Count = n() ) ) )
    
    plots = c( plots, list( rocplot.subsets( grp = for.gender.df$Label, pred = for.gender.df$Predictor, subsets = for.gender.df$Gender ) ) )
}

multiplot( plotlist = plots, file = "reports/figure4.pdf", cols=2 )