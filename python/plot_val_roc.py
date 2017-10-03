# -*- coding: utf-8 -*-
"""
Created on Wed Sep  6 16:54:04 2017

Command line utility for making Validation ROC plot

@author: Yuriy Sverchkov (yuriy.sverchkov@wisc.edu)
"""

import analysis_utilities
import logging
from sys import argv
from pickle import load
from misc_tools import long_names

# Global constants
logging.basicConfig( level = logging.DEBUG )
log = logging.getLogger(__name__)
log.setLevel( logging.DEBUG )

# Main run
if __name__ == '__main__':

#        for question, panel_size in [(1,5), (3,4)]:
    infilename = argv[1]
    outfilename = argv[2]
    withtitle = argv[3]
    
    with open( infilename, 'rb' ) as infile:
        result = load( infile )

    if withtitle == 't':
        title = "Model: "+long_names[result['method']]+"\nPanel: "+str(result['panel'])
    else:
        title = ''
    
    log.debug( 'Making pdf, model {}, panel {}'.format(long_names[result['method']],str(result['panel'])) )
    analysis_utilities.plotROCwithCRfromScores( result['score'], result['label'], plot_title = title, pdf_file = outfilename, plot = False )
