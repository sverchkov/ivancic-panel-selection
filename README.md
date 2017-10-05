# ivancic-panel-selection
Code used in the statistical analysis for "Blood serum protein biomarkers for the screening of non-metastatic colorectal carcinomas" by Melanie Ivancic et al.

## Running the code ##

This project is set up to run in a Unix-like environment (OSX or Linux)

Using `make` invokes the full process of:

* Extracting the biomarker measurements from the excel files in `raw-data`
* Computing the per-patient-sample geometric means for each biomarker across replicates
* Matching the biomarker measurements to patient diagnoses (in `raw-data/csv/labels.csv`)
* Splitting the data into training and validation according to `raw-data/csv/`
* Generating the pooled cross-validation ROC curves (these will be placed in a `reports` folder)
* Selecting the validation panel+method and producing ROC curves on the validation set (also in the `reports` folder).
* In the process of generating reports, pickled python objects containing the results are also generated (in a `python-results` folder).
* In the process of generating pooled cross-validation ROC curves, statistics about how many times each method and panel is selected are printed to the command line.

## Misc notes ##

**Random variation:** Since there is inherent randomness in the process of learning a random forest or an extremely randomized trees model, there is variation across different runs of the pipeline in the results.

