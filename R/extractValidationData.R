# Extract new validation data
# Yuriy Sverchkov

# Validation data is made up of all the samples that are neither in the (updated) training set nor any of the following labels:
#   Neuroendocrine tumor
#   Post Chemoradiation
#   Undetermined

clean.data = read.csv( "Clean_Data_csv/clean_data.csv", stringsAsFactors = FALSE )
training.data = read.csv( "Training_Data/training_data.csv", stringsAsFactors = FALSE )
validation.data = clean.data %>% filter(
  !( replicate_name %in% training.data$replicate_name ) &
  !( label %in% c( "Neuroendocrinetumor", "PostChemoradiation", "Undetermined" ) ) )

write.csv( validation.data, "Validation_Data/validation_data.csv", row.names = FALSE )