# -*- coding: utf-8 -*-
"""
Run cross-validation analysis

@author: Yuriy Sverchkov (yuriy.sverchkov@wisc.edu)
"""

from sys import argv
from pandas import read_csv
from analysis_pipeline import run_analysis_pipeline

if __name__ == '__main__':

    training_filename = argv[1]
    panel_size = int(argv[2])
    pickled_filename = argv[3]
    
    data = read_csv(training_filename)
    result = run_analysis_pipeline(
        data = data,
        panel_size = panel_size,
        output_file_name = pickled_filename
    )        
