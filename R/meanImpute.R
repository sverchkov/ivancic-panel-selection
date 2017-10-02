# Mean imputing the data
# Originally by Serge Aleshin-Guendel, adapted by Yuriy Sverchkov

#' Mean impute training data
#' This assumes that all but the last column may need to be imputed, since the last column is the label.
#' @param data a data frame of features+label
#' @return a data frame with features mean-imputed
meanImpute = function( data ){
  for(i in 1:(dim(data)[2]-1)){
    
    nas = is.na( data[i] )
    if( any( nas ) )
      data[i][ nas ] = mean( data[[i]], na.rm = TRUE )
  }
  
  data
}

#' Mean impute validation data
#' 
#' Imputed each feature in the validation data with the mean of the (observed) training data
#' This assumes that all but the last column may need to be imputed, since the last column is the label.
#' @param training.data a data frame of features+label
#' @param validation.data a data frame of features+label (must match `training.data` by column)
#' @return validation data frame with features mean-imputed using the training data mean
meanImputeValidation = function( training.data, validation.data ){

  for (i in 1:(dim(validation.data)[2]-1) ){
    
    validation.NAs = is.na( validation.data[i] )
    if (any( validation.NAs ))
      validation.data[i][ validation.NAs ] = mean( training.data[[i]], na.rm = TRUE )
  }
  
  validation.data
}
