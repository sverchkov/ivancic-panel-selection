# -*- coding: utf-8 -*-
"""
Created on Wed Sep  6 16:54:04 2017

Validation evaluation script

@author: yuriy
"""

import analysis_pipeline
import pandas
import logging
from sys import argv
from pickle import dump
from misc_tools import unpack

# Global constants
logging.basicConfig( level = logging.DEBUG )
log = logging.getLogger(__name__)
log.setLevel( logging.DEBUG )

# Main run
if __name__ == '__main__':

    training_filename = argv[1]
    validation_filename = argv[2]
    panel_size = int( argv[3] )
    pickle_filename = argv[4]

    training_data = pandas.read_csv(training_filename)
    validation_data = pandas.read_csv(validation_filename)
            
    train_features, train_labels, feature_labels = unpack( training_data )
    test_features, test_labels, feature_labels_test = unpack( validation_data )
    
    if feature_labels != feature_labels_test:
        log.error( "Feature labels don't match up between training and validation." )
    
    result = analysis_pipeline.core_pipeline( train_features, train_labels, test_features, test_labels, feature_labels, panel_size )

    log.debug( 'saving pkl' )            
    
    with open( pickle_filename, 'wb' ) as outfile:
        dump( result, outfile )