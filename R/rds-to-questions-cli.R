# Getting the validation data ready for questions 1-3 analysis, command line utility
# By Yuriy Sverchkov
# Based on code by Serge Aleshin-Guendel

library("dplyr")
# We assume the file is run in subdirectory the git project root.
source("R/meanImpute.R")

the.args <- commandArgs( TRUE )
# Argument 1: output file
# Argument 2: question #
# Argument 3: training/validation
# Argument 4: impute (omit not supported yet)
# Argument 5: training .rds file
# Argument 6: validation .rds file (if validation)

out.file <- the.args[1]
question <- the.args[2]
is.validation <- the.args[3] == "validation"
is.impute <- the.args[4] == "impute"
training <- readRDS( the.args[5] )
if( is.validation && is.impute ) validation <- readRDS( the.args[6] )

condition.filter <- switch( question,
                           q1 = c("N/A","Low","Stage 1","Stage 2","Stage 3"),
                           q2 = c("N/A","Low","High"),
                           q3 = c("Stage 1","Stage 2","Stage 3") )
condition.label <- switch( question,
                          q1 = c("Stage 1","Stage 2","Stage 3"),
                          q2 = c("High"),
                          q3 = c("Stage 3"))

specifyToQuestion <- function( data )
  data %>%
    filter( Risk.category.Cancer.stage %in% condition.filter ) %>%
    mutate( label = ifelse( Risk.category.Cancer.stage %in% condition.label, 1, 0 ) ) %>%
    select( -Sample.ID, -Master.Mix, -Risk.category.Cancer.stage, -Colonoscopy.Pathology )

training = specifyToQuestion( training )

output.data <-
  if ( is.impute ) {
    if ( is.validation ){
      meanImputeValidation( training, specifyToQuestion( validation ) )
    } else {
      meanImpute( training )
    }
  } else {
    training
  }

write.csv( output.data, file = out.file, na="", row.names = FALSE )
