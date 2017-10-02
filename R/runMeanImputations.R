# Run mean imputations
source( "R/meanImpute.R" )

s.a.f = FALSE # Global strings as factors flag

for ( q in 1:3 ){
  training.file = paste0( "Training_Data/q", q, "_data.csv" )
  validation.file = paste0( "Validation_Data/q", q, "_validation_data.csv" )
  omm.validation.file = paste0( "Validation_Data/q", q, "_omm_validation_data.csv" )
  imputed.training.file = paste0( "Training_Data/q", q, "_data_mean_imputed.csv" )
  imputed.validation.file = paste0( "Validation_Data/q", q, "_validation_data_mean_imputed.csv" )
  imputed.omm.validation.file = paste0( "Validation_Data/q", q, "_omm_validation_data_mean_imputed.csv" )
  
  q.training.data = read.csv( training.file, stringsAsFactors = s.a.f )
  q.validation.data = read.csv( validation.file, stringsAsFactors = s.a.f )
  q.omm.validation.data = read.csv( nmm.validation.file, stringsAsFactors = s.a.f )
  
  write.csv(
    meanImpute( q.training.data ),
    file = imputed.training.file,
    row.names = FALSE )
  
  write.csv(
    meanImputeValidation( q.training.data, q.validation.data ),
    file = imputed.validation.file,
    row.names = FALSE
  )
  
  write.csv(
    meanImputeValidation( q.training.data, q.omm.validation.data ),
    file = imputed.omm.validation.file,
    row.names = FALSE
  )
}