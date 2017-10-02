# -*- coding: utf-8 -*-
"""
Constants used by analysis methods

Created on Fri Aug 12 18:49:32 2016

@author: Yuriy Sverchkov
"""

import matplotlib.pyplot as plt

def q1plotpoints():
    """ Plot ROC points from existing methods for Q1 """
    plt.plot(0.18,0.92,marker='o',label="Cologuard",markersize=10,linestyle="",markerfacecolor="k")
    plt.plot(0.05,0.74,marker='^',label="FIT",markersize=10,linestyle="",markerfacecolor="k")
    plt.plot(0.20,0.68,marker='s',label="Epi proColon",markersize=10,linestyle="",markerfacecolor="k")
    plt.plot(0.22,0.81,marker='p',label="SimplyPro Colon",markersize=10,linestyle="",markerfacecolor="k")
    return
    
def q2plotpoints():
    plt.plot(0.14,0.42,marker='o',label="Cologuard",markersize=10,linestyle="",markerfacecolor="k")
    plt.plot(0.37,0.50,marker='^',label="FIT",markersize=10,linestyle="",markerfacecolor="k")
    plt.plot(0.30,0.27,marker='s',label="Epi proColon",markersize=10,linestyle="",markerfacecolor="k")
    plt.plot(0.20,0.45,marker='p',label="SimplyPro Colon",markersize=10,linestyle="",markerfacecolor="k")
    return
    
def q3plotband():
    plt.fill_between([-0.05,1.05],0.45,0.75,alpha=0.4)
    return