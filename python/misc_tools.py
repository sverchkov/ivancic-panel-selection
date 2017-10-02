# -*- coding: utf-8 -*-
"""
Miscellaneous Helper Functions and Constants

Created on Fri Sep 29 14:53:21 2017

@author: Yuriy Sverchkov (yuriy.sverchkov@wisc.edu)
"""

import numpy
from sklearn import ensemble, linear_model, svm, preprocessing, tree, naive_bayes

# Cnstants
long_names = {
    "lr":"Logistic regression",
    "lsvc":"SVC with linear kernel",
    "rbfsvc":"SVC with RBF kernel",
    "nb":"Naive Bayes",
    "dt":"Decision tree",
    "rf":"Random forest",
    "et":"Extremely randomized trees"
}

classifier_dict = {
    "lr":linear_model.LogisticRegression(),
    "lsvc":svm.SVC( kernel = "linear", probability = True ),
    "rbfsvc":svm.SVC( probability = True ),
    "nb":naive_bayes.GaussianNB(),
    "dt":tree.DecisionTreeClassifier(),
    "rf":ensemble.RandomForestClassifier( n_estimators=100 ),
    "et":ensemble.ExtraTreesClassifier( n_estimators=100 )
}

normalization_dict = {
    "lr":"scaled",
    "lsvc":"scaled",
    "rbfsvc":"scaled",
    "nb":"log"
}

feature_selection_C_methods = [
    lambda C: svm.LinearSVC( C = C, penalty = "l1", dual = False),
    lambda C: linear_model.LogisticRegression( C = C, penalty = "l1" ),
    lambda C: svm.SVC( C = C, kernel = "rbf")
]

feature_selection_tree_methods = [
    tree.DecisionTreeClassifier(),
    ensemble.RandomForestClassifier(n_estimators=100),
    ensemble.ExtraTreesClassifier(n_estimators=100)
]

# Functions
def unpack( data ):
    n_features = data.shape[1]-1
    return (
        numpy.array( data.ix[:,:n_features] ), # features
        numpy.array( data.ix[:,n_features] ), # labels
        list(data)[0:n_features] # feature labels
    )
    
def normalize_features( train_features, test_features = None, normal = None, mean_impute = True ) :

    if mean_impute:
        imputer = preprocessing.Imputer( strategy = 'mean' )
        train_features = imputer.fit_transform( train_features )
        if test_features is not None:
            test_features = imputer.transform( test_features )
    
    normal_train_features = train_features
    normal_test_features = test_features

    if(normal=="log"):
        normal_train_features = numpy.log( train_features )
        
    if(normal=="scaled"):
        scaler = preprocessing.StandardScaler()
        normal_train_features = scaler.fit_transform( train_features )
        if test_features is not None:
            normal_test_features = scaler.transform( test_features )
    
    if normal_test_features is None:
        return ( normal_train_features )
    else:
        return ( normal_train_features, normal_test_features )
