# Assuming that working directory is project root
library("psych")# For geometric.mean
source("data.cleaning.functions.R")
source("protein-short-names.R")

# Do old master mix
indir = "../Raw_Data_csv/Old_Master_Mix_Aux/"
files = paste0( indir, dir( path = indir ) )

old.mm.dfs = Map( normalizeOldMasterMixNames, Map( readCSV, files, TRUE ) )

old.mm.df = Reduce( bind_rows, old.mm.dfs )

# Fix some samples:
# Use underscores everywhere
old.mm.df = old.mm.df %>%
  mutate( Replicate.Name = gsub( "-", "_", Replicate.Name, fixed = TRUE ) )

outfile = "data-clean/old_mm_v2.rds"
saveRDS( old.mm.df, file = outfile )

# Do new master mix
indir = "../Raw_Data_csv/New_Master_Mix_Aux/"
files = paste0( indir, dir( path = indir ) )

new.mm.dfs = Map( standardizeNewMasterMixNames, Map( readCSV, files, FALSE ) )

new.mm.df = Reduce( bind_rows, new.mm.dfs )

# Fix some samples:
# 1. Date typo
new.mm.df = new.mm.df %>%
  mutate( Replicate.Name = sub( "2017_02189", "2017_0218", Replicate.Name, fixed = TRUE ) )

outfile = "data-clean/new_mm_v2.rds"
saveRDS( new.mm.df, file = outfile )

# Fill the "adjusted" column for old mm
old.mm.df = old.mm.df %>% mutate( Ratio.End.to.Ref.Adjusted = Total.Area.Endogenous / Total.Area.Reference.Standard )

# Remove omitted and merge
all.df =
  bind_rows( old.mm.df %>% mutate( Master.Mix = "old" ) %>% filter( !omitted | is.na( omitted ) )
           , new.mm.df %>% mutate( Master.Mix = "new" ) %>% filter( !is.na( Ratio.End.to.Ref ) ) )
all.df = expandReplicateName( all.df )

saveRDS( all.df, "data-clean/all.v2.rds" )

# Remove some specific sample sets
all.df = all.df %>%
  filter( !( grepl( "^9[_-]?(Post|Pre)", Sample.ID ) & ( Date == "2016-01-08") )
       || !( grepl( "^28[_-]?(Post|Pre)", Sample.ID ) & ( Date == "2016-02-16" ) )
       || !( ( Sample.ID == "31489_Ctrl" ) & ( Master.Mix == "new" ) )
        )

# Get geometric mean of each group
summarized.df = all.df %>%
  group_by( Sample.ID, Master.Mix, Risk.category.Cancer.stage, Colonoscopy.Pathology, Protein.Name, Gender, Age, Age.Bin, Polyp.Loc ) %>%
  summarise( Geom.Mean = geometric.mean( Ratio.End.to.Ref.Adjusted ) ) %>%
  ungroup() %>%
  left_join( protein.short.names, by = c( Protein.Name = "Long.name" ) ) %>%
  rename( Protein = Short.name )

# Save summarized table
saveRDS( summarized.df, "data-clean/summarized.v2.rds" )

# Flatten by converting protein names to columns
list.of.rows = Map( function( id, mm )
  summarized.df %>%
    filter( Sample.ID == id, Master.Mix == mm ) %>%
    unstack( Geom.Mean ~ Protein ) %>%
    t() %>%
    as.data.frame() %>%
    mutate( Sample.ID = id, Master.Mix = mm )
  , distinct( all.df, Sample.ID, Master.Mix )$Sample.ID
  , distinct( all.df, Sample.ID, Master.Mix )$Master.Mix )

big.df = Reduce( bind_rows, list.of.rows )

# Attach label columns to big_df
labeled.big.df = left_join(
  big.df,
  summarized.df %>% ungroup() %>% distinct( Sample.ID, Master.Mix, Risk.category.Cancer.stage, Colonoscopy.Pathology ) )

# Save as .rds
saveRDS( labeled.big.df, "data-clean/features.v2.rds" )