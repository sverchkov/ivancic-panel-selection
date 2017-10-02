# ivancic-panel-selection
Code used in the statistical analysis for "Blood serum protein biomarkers for the screening of non-metastatic colorectal carcinomas" by Melanie Ivancic et al.

## Running the code ##

Data formatting: excel files in `raw-data` are first broken up into per-sheet csv files using the script in that folder

(need to fill in details on running the R code to get rmds out of those csvs)

## Running the analysis ##

Once `R\data-clean\training.rds` and `R\data-clean\testing.rds` are created, running the makefile in the project root creates PDF reoprts of the ROC curves in a `reports` folder.
Results are saved as pickled python objects in `python-results`
