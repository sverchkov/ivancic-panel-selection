# Make Training CSV
# Use the old training data to make a table with the new IDS
library( "dplyr" )
library("gsubfn")

old.training.data = read.csv( "Training_Data/Old/training_data.csv", stringsAsFactors = FALSE )

id.map = old.training.data %>%
  select( replicate_name ) %>%
  mutate( new_name = strapply( replicate_name,
                                "^[0-9]{4}[_-][0-9]{2}[_-]?[0-9]{2}[_-]([0-9]+[_-]?[A-Za-z]+)[_-][0-9_]+$",
                                FUN = function(x) paste0( x, "_oldMM" ),
                                simplify = TRUE ) )

new.clean.data = read.csv( "Clean_Data_csv/clean_data.csv", stringsAsFactors = FALSE )
new.training.data = inner_join(
  new.clean.data,
  id.map %>% select( new_name ),
  by = c( "replicate_name" = "new_name" )
) %>% distinct( replicate_name, .keep_all = TRUE )

write.csv( new.training.data, "Training_Data/training_data.csv", na = "", row.names = FALSE )
