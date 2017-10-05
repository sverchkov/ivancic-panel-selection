library("dplyr")
library("psych")# For geometric.mean
source("R/protein-short-names.R")

# Load the data from csv, and extract individual patient sample ids
all.df <-
  read.csv( "raw-data/csv/all.csv", stringsAsFactors = FALSE ) %>% # Load data
  mutate( Sample.ID = gsub( "_[0-9](_[0-9])?$", "", Replicate.Name ) ) %>% # Strip replicate number
  mutate( Sample.ID = gsub( "[_ -]", "_", Sample.ID ) ) # Make sure we always use underscores

# Get geometric mean of each protein ratio for each sample across replicates
summarized.df = all.df %>%
  group_by( Sample.ID, Protein.Name ) %>%
  summarise( Geom.Mean = geometric.mean( Corrected.Ratio ) ) %>%
  ungroup() %>%
  left_join( protein.short.names, by = c( Protein.Name = "Long.name" ) ) %>%
  rename( Protein = HGNC.Symbol )

# Save summarized table
saveRDS( summarized.df, "rds-data/summarized.rds" )

# Flatten by converting protein names to columns
list.of.rows = Map( function( id )
  summarized.df %>%
    filter( Sample.ID == id ) %>%
    unstack( Geom.Mean ~ Protein ) %>%
    t() %>%
    as.data.frame() %>%
    mutate( Sample.ID = id )
  , distinct( all.df, Sample.ID )$Sample.ID )

features.df = Reduce( bind_rows, list.of.rows )

# Save features table
saveRDS( features.df, "rds-data/features.rds" )

# Attach class label columns
labels = read.csv( "raw-data/csv/labels.csv", stringsAsFactors = FALSE )

labeled.features.df = left_join( features.df, labels )

# Save as .rds
saveRDS( labeled.features.df, "rds-data/labeled.features.rds" )