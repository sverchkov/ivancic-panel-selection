# Makefile for running the analysis

# Python executable
PYTHON = python3

# R executable
R = rscript

# R scripts
RAW_TO_RDS = $(R) R/construct-features.R
MK_TRAINING_VALIDATION = $(R) R/make-training-and-validation.R
RCMD = $(R) R/rds-to-questions-cli.R

# Python command utilities
XLSX_TO_CSV = $(PYTHON) python/xlsx_to_single_csv.py
PLOT_CV_ROC = $(PYTHON) python/plot_cv_roc.py
PLOT_VAL_ROC = $(PYTHON) python/plot_val_roc.py
RUN_CV = $(PYTHON) python/run_cv_analysis.py
RUN_VAL = $(PYTHON) python/run_val_analysis.py

# .rds data files
RTRAINING = rds-data/training.rds
RVALIDATION = rds-data/validation.rds

# Lists
REPORT_ROCS = \
 reports/roc_cv_q1_p2.pdf\
 reports/roc_cv_q1_p3.pdf\
 reports/roc_cv_q1_p4.pdf\
 reports/roc_cv_q1_p5.pdf\
 reports/roc_cv_q2_p2.pdf\
 reports/roc_cv_q2_p3.pdf\
 reports/roc_cv_q2_p4.pdf\
 reports/roc_cv_q2_p5.pdf\
 reports/roc_cv_q3_p2.pdf\
 reports/roc_cv_q3_p3.pdf\
 reports/roc_cv_q3_p4.pdf\
 reports/roc_cv_q3_p5.pdf\
 reports/validation_q1_p2.pdf\
 reports/validation_q1_p3.pdf\
 reports/validation_q1_p4.pdf\
 reports/validation_q1_p5.pdf\
 reports/validation_q2_p2.pdf\
 reports/validation_q2_p3.pdf\
 reports/validation_q2_p4.pdf\
 reports/validation_q2_p5.pdf\
 reports/validation_q3_p2.pdf\
 reports/validation_q3_p3.pdf\
 reports/validation_q3_p4.pdf\
 reports/validation_q3_p5.pdf

PUBLISHED_FIGURES = \
 reports/roc_cv_q1_p5_clean.pdf\
 reports/roc_cv_q3_p4_clean.pdf\
 reports/validation_q1_p5_clean.pdf\
 reports/validation_q3_p4_clean.pdf\

.PHONY: all all-clean-data published-figures
.PRECIOUS:\
  python-results/roc_cv_q%_p2.pkl\
  python-results/roc_cv_q%_p3.pkl\
  python-results/roc_cv_q%_p4.pkl\
  python-results/roc_cv_q%_p5.pkl\
  python-results/validation_q%_p2.pkl\
  python-results/validation_q%_p3.pkl\
  python-results/validation_q%_p4.pkl\
  python-results/validation_q%_p5.pkl

all: analysis-reports published-figures

analysis-reports: $(REPORT_ROCS)

published-figures: $(PUBLISHED_FIGURES)

all-clean-data: plain-clean-data imputed-clean-data

plain-clean-data: q1-training.csv q2-training.csv q3-training.csv q1-validation.csv q2-validation.csv q3-validation.csv

imputed-clean-data: q1-training-imputed.csv q2-training-imputed.csv q3-training-imputed.csv q1-validation-imputed.csv q2-validation-imputed.csv q3-validation-imputed.csv

# CV pickle files

python-results/roc_cv_q%_p2.pkl: clean-data/q%-training.csv python-results
	$(RUN_CV) $< 2 $@

python-results/roc_cv_q%_p3.pkl: clean-data/q%-training.csv python-results
	$(RUN_CV) $< 3 $@

python-results/roc_cv_q%_p4.pkl: clean-data/q%-training.csv python-results
	$(RUN_CV) $< 4 $@

python-results/roc_cv_q%_p5.pkl: clean-data/q%-training.csv python-results
	$(RUN_CV) $< 5 $@

# Validation pickle files

python-results/validation_q%_p2.pkl: clean-data/q%-training.csv clean-data/q%-validation.csv
	mkdir -p $(@D)
	$(RUN_VAL) $^ 2 $@

python-results/validation_q%_p3.pkl: clean-data/q%-training.csv clean-data/q%-validation.csv
	mkdir -p $(@D)
	$(RUN_VAL) $^ 3 $@

python-results/validation_q%_p4.pkl: clean-data/q%-training.csv clean-data/q%-validation.csv
	mkdir -p $(@D)
	$(RUN_VAL) $^ 4 $@

python-results/validation_q%_p5.pkl: clean-data/q%-training.csv clean-data/q%-validation.csv
	mkdir -p $(@D)
	$(RUN_VAL) $^ 5 $@

# PDF figures in paper
reports/roc_cv_q1_p5_clean.pdf: python-results/roc_cv_q1_p5.pkl python-results
	$(PLOT_CV_ROC) $< $@

reports/validation_q1_p5_clean.pdf: python-results/validation_q1_p5.pkl python-results
	$(PLOT_VAL_ROC) python-results/validation_q1_p5.pkl reports/validation_q1_p5_clean.pdf

reports/roc_cv_q3_p4_clean.pdf: python-results/roc_cv_q3_p4.pkl python-results
	$(PLOT_CV_ROC) python-results/roc_cv_q1_p5.pkl

reports/validation_q3_p4_clean.pdf: python-results/validation_q3_p4.pkl python-results
	$(PLOT_VAL_ROC) python-results/validation_q3_p4.pkl reports/validation_q3_p4_clean.pdf

# PDF reports recipes
reports/roc_%.pdf: python-results/roc_%.pkl reports
	$(PLOT_CV_ROC) $< $@ t

reports/validation_%.pdf: python-results/validation_%.pkl reports
	$(PLOT_VAL_ROC) $< $@ t

# Directory creation recipes
clean-data python-results reports rds-data:
	mkdir -p $@

# Clean data file recipes

clean-data/q1-training-imputed.csv: clean-data $(RTRAINING)
	$(RCMD) $@ q1 training impute $(TRAINING)

clean-data/q2-training-imputed.csv: clean-data $(RTRAINING)
	$(RCMD) $@ q2 training impute $(TRAINING)

clean-data/q3-training-imputed.csv: clean-data $(RTRAINING)
	$(RCMD) $@ q3 training impute $(TRAINING)

clean-data/q1-validation-imputed.csv: clean-data $(RVALIDATION) $(RTRAINING)
	$(RCMD) $@ q1 validation impute $(RTRAINING) $(RVALIDATION)

clean-data/q2-validation-imputed.csv: clean-data $(RVALIDATION) $(RTRAINING)
	$(RCMD) $@ q2 validation impute $(TRAINING) $(VALIDATION)

clean-data/q3-validation-imputed.csv: clean-data $(RVALIDATION) $(RTRAINING)
	$(RCMD) $@ q3 validation impute $(RTRAINING) $(RVALIDATION)

clean-data/q1-training.csv: clean-data $(RTRAINING)
	$(RCMD) $@ q1 training none $(RTRAINING)

clean-data/q2-training.csv: clean-data $(RTRAINING)
	$(RCMD) $@ q2 training none $(RTRAINING)

clean-data/q3-training.csv: clean-data $(RTRAINING)
	$(RCMD) $@ q3 training none $(RTRAINING)

clean-data/q1-validation.csv: clean-data $(RVALIDATION)
	$(RCMD) $@ q1 validation none $(RVALIDATION)

clean-data/q2-validation.csv: $(VALIDATION)
	$(RCMD) $@ q2 validation none $(VALIDATION)

clean-data/q3-validation.csv: $(VALIDATION)
	$(RCMD) $@ q3 validation none $(VALIDATION)

$(VALIDATION): rds-data/labeled.features.rds raw-data/csv/training-ids.csv
	$(MK_TRAINING_VALIDATION)

rds-data/labeled.features.rds: raw-data/csv/all.csv raw-data/csv/labels.csv rds-data
	$(RAW_TO_RDS)

raw-data/csv/all.csv: raw-data/NewMMDataALL_ForPublication.xlsx raw-data/All_OldMasterMixData_For_Publication.xlsx
	$(XLSX_TO_CSV) raw-data/NewMMDataALL_ForPublication.xlsx raw-data/All_OldMasterMixData_For_Publication.xlsx -o raw-data/csv/all.csv
