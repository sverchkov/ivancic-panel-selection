# -*- coding: utf-8 -*-
"""
Yuriy Sverchkov

Implementation of confidence bands for ROC curves according to Tilbury et al.(2000).
"""

import numpy as np
import matplotlib.pyplot as plt
from math import lgamma, log
from functools import reduce
from skimage.morphology import convex_hull_image
from scipy.spatial import ConvexHull

def subexp( lnX, lnY ):
    # x-y = exp( log( 1-y/x ) + log x ) = exp( log( 1 - exp( lnY - lnX ) ) + lnX )
    if lnX < lnY: return -subexp( lnY, lnX )
    if lnX == lnY: return 0
    return np.exp( np.log( 1 - np.exp( lnY - lnX ) ) + lnX )

def ln_boundary_value( a0, a1, p ):

    if p <= 0 :
        return -np.inf
    elif p >= 1 :
        return 0
    else :
        return \
            lgamma( a0 + a1 + 2 ) \
            + reduce( np.logaddexp, [
                log( p ) * ( a0 + a1 + 1 - k ) + log( 1 - p ) * k
                - lgamma( k + 1) - lgamma( a0 + a1 + 2 - k )
                for k in range( a1 + 1 ) ], -np.inf )

def boundary_matrix( a0, a1, b0, b1, n, sorting_fix = True ):

    x_b = [ ln_boundary_value( a0, a1, i/n ) for i in range( n+1 ) ]
    y_b = [ ln_boundary_value( b0, b1, i/n ) for i in range( n+1 ) ]

    # Boundaries should be monotonically increasing but numerical instability
    # creates issues for that. Sorting should not disturb the distribution but
    # Resove instability issues.
    
    if sorting_fix :
        x_b = sorted( x_b )
        y_b = sorted( y_b )
    
    x = np.asmatrix( [ subexp( u, l ) for u,l in zip( x_b[1:], x_b[:-1] ) ] )
    y = np.asmatrix( [ subexp( u, l ) for u,l in zip( y_b[1:], y_b[:-1] ) ] )

    #x = asmatrix( exp( x_b ) )
    #y = asmatrix( exp( y_b ) )    

    # y = p( true positive )
    # x = p( false alarm )    
    
    return y.T * x
    

def rocstats( scores, labels ):

    sorted_scores = np.unique( np.append( scores, -np.inf ) )
    tp = []
    fp = []
    fn = []
    tn = []

    # Get the TP, FP, FN, and TN for each
    for score in sorted_scores:
        tp += [ sum( [ p for s,p in zip( scores, labels ) if s > score ] ) ]
        fp += [ sum( [ not p for s,p in zip( scores, labels ) if s > score ] ) ]
        fn += [ sum( [ p for s,p in zip( scores, labels ) if s <= score ] ) ]
        tn += [ sum( [ not p for s,p in zip( scores, labels ) if s <= score ] ) ]

    return ( tp, fp, fn, tn )

def roc_stats_from_counts( positives, negatives ):
    tp = []
    fp = []
    fn = []
    tn = []
    
    for i in range( len( positives )+1 ):
        tp += [ sum( positives[:i] ) ]
        fp += [ sum( negatives[:i] ) ]
        fn += [ sum( positives[i:] ) ]
        tn += [ sum( negatives[i:] ) ]
        
    return ( tp, fp, fn, tn )

def roc_surfaces( tp, fp, fn, tn, n=50 ):
    return [ boundary_matrix( a0, a1, b0, b1, n )
        for a0, a1, b0, b1
        in zip( fp, tn, tp, fn ) ]

def rocci( scores, labels, n = 50 ):
    
    tp, fp, fn, tn = rocstats( scores, labels )

    return roc_surfaces( tp, fp, fn, tn, n )
    
def plot_heatmap( heat_matrix, tpr=None, fpr=None ):

    n = len( heat_matrix )
    indeces = [ i/n for i in range( n + 1 ) ]

    plt.pcolor( indeces, indeces, np.asarray( heat_matrix ), cmap=plt.cm.Blues )

    if tpr is not None:
        plt.plot( fpr, tpr )
        
    plt.colorbar()
    
    plt.show
    plt.close
    
def plot_heatmap_only( heat_matrix ):
    m, n = heat_matrix.shape
    y = [ i/n for i in range( n + 1 ) ]
    x = [ i/m for i in range( m + 1 ) ]
    return plt.pcolormesh( x, y, np.asarray( heat_matrix ), cmap=plt.cm.Blues )
    
def confidence_blob( p_matrix, confidence = 0.95 ):
    lnconfidence = np.log( confidence )
    m, n = p_matrix.shape
    p_array = sorted( zip( np.log( np.reshape( np.asarray( p_matrix ), -1 ) ), range( m*n ) ), reverse = True )
    bin_array = [False] * (m*n)
    lnsum = None
    for lnp, i in p_array :
        if lnsum is not None and lnsum > lnconfidence :
            break
        bin_array[i] = True
        if lnsum is None:
            lnsum = lnp
        else:
            lnsum = np.logaddexp( lnsum, lnp )
        
    return np.reshape( bin_array, (m, n) )

def confidence_band( surfaces, confidence = 0.95 ):
    
    if len( surfaces ) < 2:
        return confidence_blob( surfaces[0], confidence )
        
    blobs = list( map( lambda x: confidence_blob( x, confidence ), surfaces ) )
    pairs = map( np.maximum, blobs[:-1], blobs[1:] )
    segments = map( convex_hull_image, pairs )
    return reduce( np.maximum, segments )

def get_hull_from_blob( blob ):
    
    # Get x&y
    m, n = blob.shape
    x = [ i/m for _ in range( n ) for i in range( m ) ]
    y = [ i/n for i in range( n ) for _ in range( m ) ]
    
    # Make a point set
    points = np.reshape( blob, -1 )
    x_points = np.concatenate( [ [ x_i, x_i, x_i + 1/m, x_i + 1/m ] for x_i, p in zip( x, points) if p ] )
    y_points = np.concatenate( [ [ y_i, y_i + 1/n, y_i, y_i + 1/m ] for y_i, p in zip( y, points) if p ] )
    
    # Get hull
    return ConvexHull( np.stack( [x_points, y_points], axis = 1 ) )

def plot_hull( hull, invert_x = False ):
    
    x = hull.points[ hull.vertices, 0 ]
    y = hull.points[ hull.vertices, 1 ]
    x = np.append( x, x[0] )
    y = np.append( y, y[0] )
    if invert_x:
        x = 1-x
    return plt.plot( x, y, color = '0.8' )

def plot_hulls( surfaces, invert_x = False, confidence = 0.95 ):
    for surface in surfaces :
        plot_hull( get_hull_from_blob( confidence_blob( surface, confidence ) ), invert_x )

#%% Using data from Swets 1988
if False :
    positives = [132, 85, 63, 53, 15]
    negatives = [19, 50, 48, 151, 92]
    tp, fp, fn, tn = roc_stats_from_counts( positives, negatives )
    tpr = np.divide( tp, np.add( tp, fn ) )
    fpr = np.divide( fp, np.add( fp, tn ) )
    surfaces = roc_surfaces( tp, fp, fn, tn, 500 )
    sumsurface = reduce( lambda x,y: x+y, surfaces ) / len(surfaces)
    plot_heatmap( confidence_blob( surfaces[0] ), tpr, fpr )

#%% Max heatmap
if False :
    maxsurface = np.maximum.reduce( surfaces )
    plot_heatmap( maxsurface, tpr, fpr )

#%% Basic Testing
if False :
    scores = [0.1, 0.2, 0.7, 0.4, 0.5, 0.8, 0.7, 0.9]
    labels = [0, 0, 0, 0, 1, 1, 1, 1]
    tp, fp, fn, tn = rocstats( scores, labels )
    tpr = np.divide( tp, np.add( tp, fn ) )
    fpr = np.divide( fp, np.add( fp, tn ) )
    surfaces = rocci( scores, labels, n=500 )
    sumsurface = reduce( lambda x,y: x+y, surfaces ) / len(surfaces)
    plot_heatmap( sumsurface, tpr, fpr )
