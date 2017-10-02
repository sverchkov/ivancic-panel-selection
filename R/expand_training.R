# Training set augmentation script.
# This augments the old training set with a fraction (<=0.3) of the new master mix data
# Yuriy Sverchkov
library("dplyr")
library("gsubfn")

# Load the feature table
features.df = readRDS( "data-clean/features.v2.rds" )

# Select the subset of new mm samples to set as training
training.ids = Reduce( c, Map( function ( labelset ){
  ids = filter( features.df, Risk.category.Cancer.stage %in% labelset, Master.Mix == "new" )$Sample.ID
  sample( ids, ceiling( length( ids ) * 0.3 ), replace = FALSE )
}, list( c( "Low", "N/A" ), "High" ) ) )

# Save
saveRDS( training.ids, "intermediates/nmm-training-ids.rds" )

# Load the old training data
old.training.data = read.csv( "../Training_Data/Old/training_data.csv", stringsAsFactors = FALSE )

# Extract sample ids for old data (136 IDs)
training.ids.from.old = strapplyc( old.training.data$replicate_name,
           "^[0-9]{4}[_-][0-9]{2}[_-]?[0-9]{2}[_-]([0-9]+[_-]?[A-Za-z]+)[_-][0-9_]+$",
           simplify = TRUE )

training.ids = c( training.ids, unique( training.ids.from.old ) )

# Save
saveRDS( training.ids, "intermediates/training-ids.rds" )

# Make a training set and a validation set
training.df = features.df %>% filter( Sample.ID %in% training.ids )
validation.df = features.df %>% filter(
  !( Sample.ID %in% training.ids ) &
  !( Risk.category.Cancer.stage %in% c( "Neuroendocrine tumor", "Post Chemoradiation", "Undetermined" ) ) )

# Save
saveRDS( training.df, "data-clean/training.rds" )
saveRDS( validation.df, "data-clean/validation.rds" )

## !! There are many duplicates in the training id list.
## we need to figure out why.
#(training.ids %in% features.df$Sample.ID)
#mapping = old.training.data %>% mutate( Sample.ID = training.ids.from.old )
