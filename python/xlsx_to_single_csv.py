# -*- coding: utf-8 -*-
"""
Created on Wed Oct  4 10:22:49 2017

Converting excel files to csv

@author: Yuriy Sverchkov
"""

import logging
from sys import argv
from pandas import read_excel, concat

# Constants
logging.basicConfig( level = logging.DEBUG )
log = logging.getLogger(__name__)
log.setLevel( logging.DEBUG )

standardized_columns = {
    0:'Protein Name',
    1:'Replicate Name',
    2:'Peptide Sequence',
    3:'Total Area Endogenous',
    4:'Total Area Reference Standard',
    5:'Endogenous to Reference Ratio',
    6:'Corrected Ratio'
}
# Functions
def standardize_names( df ):
    
    if len(df.columns) == 6:
        df['Corrected Ratio'] = df[df.columns[5]] # The for old master mix the corrected ratio is the raw ratio

    converter = { df.columns[i] : standardized_columns[i] for i in range(0,7) }
    
    return( df.rename( columns = converter ) )

# Main run
if __name__ == '__main__':

    workbook_files = []
    reading_flag = True    
    for arg in argv:
        if arg == argv[0]:
            continue
        
        if reading_flag:
            if arg != "-o":
                workbook_files.append( arg )
            else:
                reading_flag = False
        else:
             output_file = arg
             break

    log.debug( 'Reading workbooks: {}; Writing csv: {}'.format( str( workbook_files ), output_file ) )

    dataframes = []
    
    for workbook_file in workbook_files:
        log.debug( 'Reading {}'.format( workbook_file ) )
        dataframes += list( read_excel( workbook_file, sheetname = None ).values() )
        log.debug( 'Read successfully' )
       
    log.debug( 'Composing one large dataframe' )
    big_df = concat( map( standardize_names, dataframes ) )
    
    log.debug( 'Writing to {}'.format( output_file ) )
    big_df.to_csv( path_or_buf = output_file, index = False )
