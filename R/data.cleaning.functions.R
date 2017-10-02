library("dplyr")
library("gsubfn")

readCSV = function ( filename, has.omitted = TRUE ){
  
  df = read.csv( file = filename, stringsAsFactors = FALSE, na.strings = "#N/A" )
  
  fill.columns =
    intersect( c( "Risk.category.Cancer.stage", "Colonoscopy.Pathology", "Gender", "Age", "Age.Bin", "Polyp.Location.s." ),
               names( df ) )
  
  if( !( "X.1" %in% names( df ) ) & has.omitted ){
    df$omitted = FALSE
    has.omitted = FALSE
  }
  
  if( has.omitted ){
    df = df %>% mutate( omitted = ( tolower( X.1 ) == "omitted" ) )
    fill.columns = c( fill.columns, "omitted" )
  }
  
  for ( row in 1:nrow( df ) )
    if ( df$Risk.category.Cancer.stage[row] == "" )
      df[ row, fill.columns ] = df[ row-1, fill.columns ]
  
  df
}

normalizeOldMasterMixNames = function( df ) {
  names( df )[ c(4,5,6) ] = c("Total.Area.Endogenous","Total.Area.Reference.Standard","Ratio.End.to.Ref")
  df %>%
    select( Protein.Name
          , Replicate.Name
          , Peptide.Sequence
          , Total.Area.Endogenous
          , Total.Area.Reference.Standard
          , Ratio.End.to.Ref
          , Risk.category.Cancer.stage
          , Colonoscopy.Pathology
          , Gender
          , Age
          , Age.Bin
          , Polyp.Loc = Polyp.Location.s.
          , omitted )
}

standardizeNewMasterMixNames = function( df ){
  names( df )[ c( 6, 7 ) ] = c( "Ratio.End.to.Ref", "Ratio.End.to.Ref.Adjusted" );
  df %>% select( Protein.Name
                 , Replicate.Name
                 , Peptide.Sequence
                 , Total.Area.Endogenous
                 , Total.Area.Reference.Standard
                 , Ratio.End.to.Ref
                 , Ratio.End.to.Ref.Adjusted
                 , Risk.category.Cancer.stage
                 , Colonoscopy.Pathology )
}

#' Extract from the replicate, the date and Sample ID.
#' Assuming that the Replicate.Name is of the form YYYY_MMDD_SampleID_Replicate#
#' Assuming Replicate # to always be preceeded by _ and be numeric
expandReplicateName = function( df ){
  # Extract Year, Month, Day, ID
  # Regex parts:
  #   Beginning of line:                                ^
  #   Year:                                             ([0-9]{4})
  #   Separator:                                        [_-]
  #   Month:                                            ([0-9]{2})
  #   Separator (optional):                             [_-]?
  #   Day:                                              ([0-9]{2})
  #   Separator:                                        [_-]
  #   Numeric sample ID part:                           ([0-9]+
  #   Separator (optional):                             [_-]?
  #   Alphabetic sample ID part (Cancer/Pre/Ctrl/ etc): [A-Za-z]+)
  #   Separator:                                        [_-]
  #   Replicate number:                                 [0-9_]+
  elements = strapplyc( df$Replicate.Name, "^([0-9]{4})[_-]([0-9]{2})[_-]?([0-9]{2})[_-]([0-9]+[_-]?[A-Za-z]+)[_-][0-9_]+$", simplify = TRUE )
  
  # Add to dataframe
  df %>% mutate( Date = as.Date( paste0( elements[1,], "-", elements[2,], "-", elements[3,]) )
                 , Sample.ID = elements[4,] )
}
