# Yuriy Sverchkov
library("dplyr")

labeled.features.df <- readRDS( "rds-data/labeled.features.rds" )
training.ids <- read.csv( "raw-data/csv/training-ids.csv", stringsAsFactors = FALSE )

features.df <- left_join( labeled.features.df, training.ids )

# Make a training set and a validation set
training.df <- features.df %>% filter( Training ) %>% select( -Training )
validation.df <- features.df %>%
  filter(
    !Training &
    !( Risk.or.Stage %in% c( "Neuroendocrine tumor", "Post Chemoradiation", "Undetermined" ) ) )%>%
  select( -Training )

# Save
saveRDS( training.df, "rds-data/training.rds" )
saveRDS( validation.df, "rds-data/validation.rds" )
