#Serge Aleshin-Guendel
#Utilities!!!
#
#

import numpy
import matplotlib.pyplot as plt
import roc_ci
from sklearn.metrics import roc_curve, auc
from sklearn.cross_validation import LeaveOneOut
from sklearn import preprocessing
from matplotlib.backends.backend_pdf import PdfPages

#Generate an ROC Curve 
def plotROC( fpr, tpr, roc_auc, plot_title, plot = True, pdf_file = None, plotover = None, plotunder = None ):
    fig = plt.figure(figsize=(8, 8))
    if plotunder is not None:
        plotunder()
    plt.grid()
    plt.plot(1-fpr, tpr, lw=2, label='AUC = %0.2f' % (roc_auc))
    plt.plot([1, 0], [0, 1], '--', color=(0.6, 0.6, 0.6))
    if plotover is not None:
        plotover();
    plt.xlim([-0.05, 1.05])
    plt.ylim([-0.05, 1.05])
    plt.xticks( numpy.arange(0, 1.05, 0.1) )
    plt.yticks( numpy.arange(0, 1.05, 0.1) )
    plt.xlabel('Specificity', fontsize=16)
    plt.ylabel('Sensitivity', fontsize=16)
    plt.title( plot_title, fontsize=16)
    plt.legend(loc="lower right",numpoints=1)
    plt.gca().invert_xaxis()
    plt.gca().set_aspect('equal')
    if plot :
        plt.show()
    if pdf_file is not None :
        with PdfPages( pdf_file ) as pdf:
            pdf.savefig( fig )
    plt.close()
    
def plotROCwithCRfromScores( scores, labels, plot_title = None, plot = True, pdf_file = None, plotover = None ):
    """Plot ROC with confidence regions on points, from the classifier scores and true labels."""
    tp, fp, fn, tn = roc_ci.rocstats( scores, labels )
    tpr = numpy.divide( tp, numpy.add( tp, fn ) )
    fpr = numpy.divide( fp, numpy.add( fp, tn ) )
    auroc = auc( fpr, tpr )
    confidence_surfaces = roc_ci.roc_surfaces( tp, fp, fn, tn, n=300 )
    
    plotROC(
        fpr,
        tpr,
        auroc,
        plot_title,
        plot,
        pdf_file,
        plotover,
        plotunder = lambda : roc_ci.plot_hulls( confidence_surfaces, invert_x = True ) )    
    
def plotROCPDF(fpr, tpr,roc_auc, classifier_name,plot):
    with PdfPages('/Users/serge/Downloads/Summer/Presentation/q1_svm_cv.pdf') as pdf:
        fig= plt.figure(figsize=(8, 8))
        plt.grid()
        plt.plot(fpr, tpr, lw=2, label='AUC = %0.2f' % (roc_auc))
        plt.plot([0, 1], [0, 1], '--', color=(0.6, 0.6, 0.6))
        plt.plot(0.18,0.92,marker='o',label="Cologuard",markersize=10,linestyle="",markerfacecolor="k")
        plt.plot(0.05,0.74,marker='^',label="FIT",markersize=10,linestyle="",markerfacecolor="k")
        plt.plot(0.20,0.68,marker='s',label="Epi proColon",markersize=10,linestyle="",markerfacecolor="k")
        plt.plot(0.22,0.81,marker='p',label="SimplyPro Colon",markersize=10,linestyle="",markerfacecolor="k")
        plt.xlim([-0.05, 1.05])
        plt.ylim([-0.05, 1.05])
        plt.xticks(numpy.arange(0, 1.05, 0.1))
        plt.yticks(numpy.arange(0, 1.05, 0.1))
        plt.xlabel('1 - Specificty', fontsize=16)
        plt.ylabel('Sensitivity', fontsize=16)
        plt.title('Cross Validation ROC curve for '+classifier_name ,fontsize=16)
        plt.legend(loc="lower right",numpoints=1)
        pdf.savefig(fig)
        plt.close()

#Preform loo CV for all classfiers but SVMs
def generateROC(cv, classifier, features, labels, classifier_name, normal = None, plot = True, pdf_file = None, plotover = None ):
    pool=numpy.zeros((len(labels), 2))
    normal_features=features
    if(normal=="log"):
        normal_features=numpy.log(normal_features)
    if(normal=="scaled"):
        scaler=preprocessing.StandardScaler()
        normal_features=scaler.fit_transform(normal_features)
    for i, (train, test) in enumerate(cv):
        classifier.fit(normal_features[train], labels[train])
        probas_ = classifier.predict_proba(normal_features[test])
        pool[i,0]=labels[test]
        pool[i,1]=probas_[0,1]
    plotROCwithCRfromScores( pool[:,1], [ x == 1 for x in pool[:,0] ], classifier_name, plot, pdf_file, plotover )
    
#Preform loo CV for all classfiers but SVMs
def generateROCcoef(cv, classifier, features, labels, classifier_name, normal=None,plot=True):
    pool=numpy.zeros((len(labels), 2))
    coefs=numpy.zeros((numpy.shape(features)[1], len(labels)))
    normal_features=features
    if(normal=="log"):
        normal_features=numpy.log(normal_features)
    if(normal=="scaled"):
        scaler=preprocessing.StandardScaler()
        normal_features=scaler.fit_transform(normal_features)
    for i, (train, test) in enumerate(cv):
        classifier.fit(normal_features[train], labels[train])
        coef= classifier.coef_
        for j in range(numpy.shape(features)[1]):
            coefs[j,i]=coef[0,j]
        probas_ = classifier.predict_proba(normal_features[test])
        pool[i,0]=labels[test]
        pool[i,1]=probas_[0,1]
    fpr, tpr, thresholds = roc_curve(pool[:,0], pool[:,1])
    roc_auc = auc(fpr, tpr)
    plotROC(fpr, tpr,roc_auc, classifier_name,plot)
    return (coefs,roc_auc)

#Preform loo CV for SVMs
def generateROCdf( cv, classifier, features, feature_names, labels, classifier_name, normal = None, plot = True, pdf_file = None, plotover = None):
    pool=numpy.zeros((len(labels), 2))
    normal_features=features
    if(normal=="log"):
        normal_features=numpy.log(normal_features)
    if(normal=="scaled"):
        scaler=preprocessing.StandardScaler()
        normal_features=scaler.fit_transform(normal_features)
    for i, (train, test) in enumerate(cv):
        classifier.fit(normal_features[train], labels[train])
        df = classifier.decision_function(normal_features[test])
        pool[i,0]=labels[test]
        pool[i,1]=df[0]
    plotROCwithCRfromScores( pool[:,1], [ x == 1 for x in pool[:,0] ], classifier_name, plot, pdf_file, plotover )

#Preform loo CV for SVMs
def generateROCdfcoef(cv, classifier, features, feature_names, labels, classifier_name, normal=None,plot=True):
    pool=numpy.zeros((len(labels), 2))
    coefs=numpy.zeros((len(feature_names), len(labels)))
    normal_features=features
    if(normal=="log"):
        normal_features=numpy.log(normal_features)
    if(normal=="scaled"):
        scaler=preprocessing.StandardScaler()
        normal_features=scaler.fit_transform(normal_features)
    for i, (train, test) in enumerate(cv):
        classifier.fit(normal_features[train], labels[train])
        coef= classifier.coef_
        for j in range(len(feature_names)):
            coefs[j,i]=coef[0,j]
        df = classifier.decision_function(normal_features[test])
        pool[i,0]=labels[test]
        pool[i,1]=df[0]
    fpr, tpr, thresholds = roc_curve(pool[:,0], pool[:,1])
    roc_auc = auc(fpr, tpr)
    plotROC(fpr, tpr,roc_auc, classifier_name,plot)
    return (coefs,roc_auc)

#Preform loo CV and get feature importance for random forests and extra trees
def generateROCTrees(cv, classifier, features, labels, classifier_name, normal=None,plot=True):
    feature_importance=numpy.zeros((numpy.shape(features)[1],len(labels)))
    pool=numpy.zeros((len(labels), 2))
    normal_features=features
    if(normal=="log"):
        normal_features=numpy.log(normal_features)
    if(normal=="scaled"):
        scaler=preprocessing.StandardScaler()
        normal_features=scaler.fit_transform(normal_features)
    for i, (train, test) in enumerate(cv):
        classifier.fit(normal_features[train], labels[train])
        importances = classifier.feature_importances_
        for j in range(numpy.shape(features)[1]):
            feature_importance[j,i]=importances[j]
        probas_ = classifier.predict_proba(normal_features[test])
        pool[i,0]=labels[test]
        pool[i,1]=probas_[0,1]
    fpr, tpr, thresholds = roc_curve(pool[:,0], pool[:,1])
    roc_auc = auc(fpr, tpr)
    plotROC(fpr, tpr,roc_auc, classifier_name,plot)
    return feature_importance    

#Nested CV for Logistic Regression w/ l1 penalty
def nestedCVLR(features, labels, classifier_name, normal=None,plot=True):
    looOuter= LeaveOneOut(len(labels))
    poolOuter=numpy.zeros((len(labels), 2))
    Cs=numpy.zeros((len(labels)))
    normal_features=features
    if(normal=="log"):
        normal_features=numpy.log(normal_features)
    if(normal=="scaled"):
        scaler=preprocessing.StandardScaler()
        normal_features=scaler.fit_transform(normal_features)
    #How good is the method in the outer loop (LR) at predicting cancer?
    for i, (trainOuter, testOuter) in enumerate(looOuter):
        outerFeaturesTrain=normal_features[trainOuter]
        outerLabelsTrain=labels[trainOuter]
        #What is the lr model with the best hyperparameter settings to predict the  
        #test sample from the training samples?
        best_auc=0
        best_c=0
        lessThanOneC=numpy.arange(0.01,1.0,0.01)
        greaterThanOneC=numpy.arange(1,101,1)
        for innerC in numpy.nditer(numpy.concatenate((lessThanOneC,greaterThanOneC))):
            #How good is the model with this hyperparameter?
            looInner=LeaveOneOut(len(outerLabelsTrain))
            poolInner=numpy.zeros((len(outerLabelsTrain), 2))
            for j, (trainInner, testInner) in enumerate(looInner):
                innerFeaturesTrain=outerFeaturesTrain[trainInner]
                innerLabelsTrain=outerLabelsTrain[trainInner]
                innerModel=linear_model.LogisticRegression(penalty="l1",C=float(innerC))
                innerModel.fit(innerFeaturesTrain,innerLabelsTrain)
                probInner = innerModel.predict_proba(outerFeaturesTrain[testInner])
                poolInner[j,0]=outerLabelsTrain[testInner]
                poolInner[j,1]=probInner[0,1]
            fpr, tpr, thresholds = roc_curve(poolInner[:,0], poolInner[:,1])
            roc_auc = auc(fpr, tpr)
            if(roc_auc>best_auc):
                best_auc=roc_auc
                best_c=float(innerC)
        print( "C chosen for " + str(i)+ ": "+str(best_c) )
        Cs[i]=best_c
        bestCModel=linear_model.LogisticRegression(penalty="l1",C=best_c)
        bestCModel.fit(outerFeaturesTrain, outerLabelsTrain)
        probOuter = bestCModel.predict_proba(normal_features[testOuter])
        poolOuter[i,0]=labels[testOuter]
        poolOuter[i,1]=probOuter[0,1]
    fpr, tpr, thresholds = roc_curve(poolOuter[:,0], poolOuter[:,1])
    roc_auc = auc(fpr, tpr)
    plotROC(fpr, tpr,roc_auc, classifier_name,plot)
    return Cs  
    
#Nested CV for SVM
def nestedCVSVM(features, labels, classifier_name, normal=None,plot=True, rbf=False):
    looOuter= LeaveOneOut(len(labels))
    poolOuter=numpy.zeros((len(labels), 2))
    Cs=numpy.zeros((len(labels)))
    normal_features=features
    if(normal=="log"):
        normal_features=numpy.log(normal_features)
    if(normal=="scaled"):
        scaler=preprocessing.StandardScaler()
        normal_features=scaler.fit_transform(normal_features)
    #How good is the method in the outer loop (LR) at predicting cancer?
    for i, (trainOuter, testOuter) in enumerate(looOuter):
        outerFeaturesTrain=normal_features[trainOuter]
        outerLabelsTrain=labels[trainOuter]
        #What is the lr model with the best hyperparameter settings to predict the  
        #test sample from the training samples?
        best_auc=0
        best_c=0
        lessThanOneC=numpy.arange(0.01,1.0,0.01)
        greaterThanOneC=numpy.arange(1,101,1)
        for innerC in numpy.nditer(numpy.concatenate((lessThanOneC,greaterThanOneC))):
            #How good is the model with this hyperparameter?
            looInner=LeaveOneOut(len(outerLabelsTrain))
            poolInner=numpy.zeros((len(outerLabelsTrain), 2))
            for j, (trainInner, testInner) in enumerate(looInner):
                innerFeaturesTrain=outerFeaturesTrain[trainInner]
                innerLabelsTrain=outerLabelsTrain[trainInner]
                innerModel=svm.LinearSVC(penalty="l1", dual=False,C=float(innerC))
                if rbf==True:
                    innerModel=svm.SVC(kernel='rbf',C=float(innerC))
                innerModel.fit(innerFeaturesTrain,innerLabelsTrain)
                dfInner = innerModel.decision_function(outerFeaturesTrain[testInner])
                poolInner[j,0]=outerLabelsTrain[testInner]
                poolInner[j,1]=dfInner[0]
            fpr, tpr, thresholds = roc_curve(poolInner[:,0], poolInner[:,1])
            roc_auc = auc(fpr, tpr)
            if(roc_auc>best_auc):
                best_auc=roc_auc
                best_c=float(innerC)
        print( "C chosen for " + str(i)+ ": "+str(best_c) )
        Cs[i]=best_c
        bestCModel=svm.LinearSVC(penalty="l1", dual=False,C=best_c)
        if rbf==True:
            bestCModel=svm.SVC(kernel='rbf',C=best_c)
        bestCModel.fit(outerFeaturesTrain, outerLabelsTrain)
        dfOuter = bestCModel.decision_function(normal_features[testOuter])
        poolOuter[i,0]=labels[testOuter]
        poolOuter[i,1]=dfOuter[0]
    fpr, tpr, thresholds = roc_curve(poolOuter[:,0], poolOuter[:,1])
    roc_auc = auc(fpr, tpr)
    plotROC(fpr, tpr,roc_auc, classifier_name,plot)
    return Cs
    
    