# -*- coding: utf-8 -*-
"""
Created on Tue Aug 29 18:17:46 2017

Automated feature and model selection with full pipline nested within loocv

@author: Yuriy Sverchkov (yuriy.sverchkov@wisc.edu)
"""

import pandas
import numpy
import roc_ci
import logging
import functools
import misc_tools as mt
#import analysis_utilities as util
from pickle import dump
from multiprocessing import Pool
from sklearn.feature_selection import SelectFromModel
from sklearn.cross_validation import LeaveOneOut

# Global constants
logging.basicConfig( level = logging.DEBUG )
log = logging.getLogger(__name__)
log.setLevel( logging.DEBUG )

max_fpr = 0.2 # We are interested in maximizing the TPR only below this FPR

# Functions
   
def get_C_panel( method, features, labels, C ):
    model = SelectFromModel( method(C).fit( mt.normalize_features( features, normal="scaled" ), labels ), prefit = True )
    return ( model.get_support( True ) )

def filter_C_panels( feature_selection_function, C_range = numpy.nditer( numpy.arange(0.001,1.0,0.001) ), panel_size = 5 ):
    panels = map( frozenset, map( feature_selection_function, C_range ) )
    seen = set()
    return( [panel for panel in panels if len( panel ) == panel_size and not ( panel in seen or seen.add( panel ) ) ] )

def tree_panel( model, panel_size ):
    fs, importances =  zip( *sorted( enumerate( model.feature_importances_ ), key = lambda item: -item[1] ) )
    return( frozenset( fs[0:panel_size] ) )
   
def get_panel_set( features, labels, panel_size ):

    panels = set()
    
    # Get L1 panels
    for method in mt.feature_selection_C_methods:
        panels.update( filter_C_panels( lambda C : get_C_panel( method, features, labels, C ), panel_size = panel_size ) )
    # Get Tree panels
    for method in mt.feature_selection_tree_methods:
        panels.add( tree_panel( method.fit( mt.normalize_features( features ), labels ), panel_size ) )
    # Convert to list of lists
    return ( list( map( list, panels ) ) )

def core_pipeline( train_features, train_labels, test_features, test_labels, feature_labels, panel_size, random_seed = None ):

    # save or set seed
    if random_seed is not None:
        numpy.random.set_state( random_seed )
    else:
        random_seed = numpy.random.get_state()    

    n = len( train_features )    
    
    best_panel = None
    best_method = None
    best_inner_scores = None
    best_inner_labels = None
    best_score = 0
    
    # Begin Panel+method Selection
    for panel in get_panel_set( train_features, train_labels, panel_size ):

        panel_features = train_features[:,panel]
    
        for method, classifier in mt.classifier_dict.items():
            
            # Prepare arrays for result
            inner_labels = numpy.zeros((n, 1))
            inner_scores = numpy.zeros((n, 1))
                    
            for j, (inner_train, inner_test) in enumerate( LeaveOneOut( n ) ):
                
                normalized_train, normalized_test = mt.normalize_features( panel_features[inner_train], panel_features[inner_test] )
           
                model = classifier.fit( normalized_train, train_labels[ inner_train ] )
                probabilities = model.predict_proba( normalized_test )
                
                # Record test label, test score, panel
                inner_scores[j,0] = probabilities[0,1]
                inner_labels[j,0] = train_labels[ inner_test ]
            
            # Get the ROC    
            tp, fp, fn, tn = roc_ci.rocstats( inner_scores, inner_labels )
            tpr = numpy.divide( tp, numpy.add( tp, fn ) )
            fpr = numpy.divide( fp, numpy.add( fp, tn ) )
        
            panel_method_score = numpy.max( [tpr[i] for i in range( 0, len(tpr) ) if fpr[i] <= max_fpr] )

            if panel_method_score > best_score:
                best_panel = panel
                best_method = method
                best_score = panel_method_score
                best_inner_scores = inner_scores
                best_inner_labels = inner_labels
    # End Panel+Method Selection
                
    classifier = mt.classifier_dict[ best_method ]
    
    # Normalize the data
    normalized_train, normalized_test = mt.normalize_features( train_features[:,best_panel], test_features[:,best_panel], normal = mt.normalization_dict.get( best_method ) )
 
    model = classifier.fit( normalized_train, train_labels )                
    probabilities = model.predict_proba( normalized_test )
        
    # Record test label, test score
    return ( {
        'panel': [ feature_labels[i] for i in best_panel ],
        'method': best_method,
        'score': probabilities[:,1],
        'label': test_labels,
        'inner_scores': best_inner_scores,
        'inner_labels': best_inner_labels,
        'random_state': random_seed
    } )
    
    
def outer_cv_fold( train_test, features, labels, feature_labels, panel_size ):
    train, test = train_test
    return ( core_pipeline( features[train], labels[train], features[test], labels[test], feature_labels, panel_size ) )
    
def run_analysis_pipeline( data, panel_size, output_file_name = None ):
    
    log.debug( "Panel size %d", panel_size )
    
    n = data.shape[0]
    n_features = data.shape[1]-1
    feature_labels = list(data)[0:n_features]
    features = numpy.array( data.ix[:,:n_features] )
    labels = numpy.array( data.ix[:,n_features] )

    the_cv_fold = functools.partial( outer_cv_fold, features = features, labels = labels, feature_labels = feature_labels, panel_size = panel_size )
    
    with Pool(10) as p:
        results = p.map( the_cv_fold, LeaveOneOut(n) )

    if output_file_name is not None:
        with open( output_file_name, 'wb') as outfile:
            dump( list( results ), outfile )
            
        log.debug( "Panel size %d results saved", question, panel_size )
    
    return ( results )

# Main run
if __name__ == '__main__':

    log.warning( 'Running analysis_pipeline.py directly is deprecated, it is recommended to run run_cv_analysis.py with command line arguments.')

    log.debug( 'Running' )    
    
    for question in [1,2,3]:
        
        log.debug( "Question %d", question )
        
        data = pandas.read_csv('../clean-data/q'+str(question)+'-training.csv')

        for panel_size in [2,3,4,5]:
            result = run_analysis_pipeline(
                data = data,
                panel_size = panel_size,
                output_file_name = 'results/roc_results_q'+str(question)+'_p'+str(panel_size)+'.pkl'
            )        
            log.info( str( result ) )
    # Get the ROC    
#    tp, fp, fn, tn = roc_ci.rocstats( roc_scores, roc_labels )
#    tpr = numpy.divide( tp, numpy.add( tp, fn ) )
#    fpr = numpy.divide( fp, numpy.add( fp, tn ) )
#    
#    util.plotROCwithCRfromScores( roc_scores, roc_labels, plot_title = "Panel size "+str(panel_size) )
    #return( numpy.max( [tpr[i] for i in range( 0, len(tpr) ) if fpr[i] <= 0.2] ) )