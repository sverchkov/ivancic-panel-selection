# -*- coding: utf-8 -*-
"""
Created on Mon Sep  4 11:11:37 2017

Analyzing results

@author: Yuriy Sverchkov
"""

import logging
import analysis_utilities
import numpy
from sys import argv
from pickle import load

# Global constants
logging.basicConfig( level = logging.INFO )
log = logging.getLogger(__name__)
log.setLevel( logging.INFO )

# Functions
def inc( count_dict, key ):
    value = count_dict.get( key )
    if value is None:
        value = 0
    value += 1
    count_dict[key] = value
    return ( count_dict )

def plot_roc_curve( result_list, title = None, output_filename = None ):

    scores, labels = map( lambda x : numpy.squeeze( numpy.array( x ) ), zip( * [ (r['score'], r['label']) for r in result_list ] ) )
    
    log.debug( 'Scores for ROC "'+str(title) + '": '+str(scores) )
    log.debug( 'Labels for ROC "'+str(title) + '": '+str(labels) )

    analysis_utilities.plotROCwithCRfromScores( scores, labels, plot_title = title, pdf_file = output_filename, plot = False )
    
def get_best_method_panel( result_list ):
    
    count_both = dict()
    count_methods = dict()
    count_panels = dict()

    for point in result_list :
        method = point['method']
        inc( count_methods, method )
        panel = frozenset( point['panel'] )
        inc( count_panels, panel )
        key = (method, panel )
        inc( count_both, key )

    sorted_both = sorted( count_both.items(), key = lambda t: -t[1] )
    sorted_methods = sorted( count_methods.items(), key = lambda t: -t[1] )
    sorted_panels = sorted( count_panels.items(), key = lambda t: -t[1] )
    
    log.info( 'Count tables' )
    # Pretty print both
    for (method, panel), count in sorted_both:
        log.info( ' {:3} {:7} {}'.format( count, method, tuple(panel) ) )
    
    # Prety print methods
    for method, count in sorted_methods:
        log.info( ' {:3} {:7}'.format( count, method ) )
        
    # Pretty print panels 
    for panel, count in sorted_panels:
        log.info( ' {:3} {}'.format( count, tuple(panel) ) )

    best_pair_method, best_pair_panel = sorted_both[0][0]
    best_method = sorted_methods[0][0]
    best_panel = sorted_panels[0][0]
    
    if best_pair_method != best_method:
        log.warning( "Best pair's method (%s) is different from best individual method (%s)", best_pair_method, best_method )

    if best_pair_panel != best_panel:
        log.warning( "Best pair's panel (%s) is different from best individual panel (%s)", best_pair_panel, best_panel )
    
    return ( best_method, best_panel )

# Main run
if __name__ == '__main__':

    results_filename = argv[1]
    pdf_filename = argv[2]
    maketitle = argv[3]

    with open( results_filename, 'rb' ) as infile:
        result = load( infile )

    panel_size = len( result[0]['panel'] )

    if maketitle == 't':
        title = 'Panel size {}'.format( panel_size )
    else:
        title = ''

    plot_roc_curve( result, title = title, output_filename = pdf_filename )
    method, panel = get_best_method_panel( result )
    log.info( 'Best method, panel: '+str( (method, panel ) ) )
