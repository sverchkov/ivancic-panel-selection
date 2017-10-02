# Makefile for R data processing, creating files for python
RCMD = rscript R/rds-to-questions-cli.R
RTRAINING = R/data-clean/training.rds
RVALIDATION = R/data-clean/validation.rds
PYTHON = python3
PLOT_CV_ROC = python/plot_cv_roc.py
PLOT_VAL_ROC = python/plot_val_roc.py
RUN_CV = python/run_cv_analysis.py
RUN_VAL = python/run_val_analysis.py
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
	$(PYTHON) $(RUN_CV) $< 2 $@

python-results/roc_cv_q%_p3.pkl: clean-data/q%-training.csv python-results
	$(PYTHON) $(RUN_CV) $< 3 $@

python-results/roc_cv_q%_p4.pkl: clean-data/q%-training.csv python-results
	$(PYTHON) $(RUN_CV) $< 4 $@

python-results/roc_cv_q%_p5.pkl: clean-data/q%-training.csv python-results
	$(PYTHON) $(RUN_CV) $< 5 $@

# Validation pickle files

python-results/validation_q%_p2.pkl: clean-data/q%-training.csv clean-data/q%-validation.csv
	mkdir -p $(@D)
	$(PYTHON) $(RUN_VAL) $^ 2 $@

python-results/validation_q%_p3.pkl: clean-data/q%-training.csv clean-data/q%-validation.csv
	mkdir -p $(@D)
	$(PYTHON) $(RUN_VAL) $^ 3 $@

python-results/validation_q%_p4.pkl: clean-data/q%-training.csv clean-data/q%-validation.csv
	mkdir -p $(@D)
	$(PYTHON) $(RUN_VAL) $^ 4 $@

python-results/validation_q%_p5.pkl: clean-data/q%-training.csv clean-data/q%-validation.csv
	mkdir -p $(@D)
	$(PYTHON) $(RUN_VAL) $^ 5 $@

# PDF figures in paper
reports/roc_cv_q1_p5_clean.pdf: python-results/roc_cv_q1_p5.pkl python-results
	$(PYTHON) $(PLOT_CV_ROC) $< $@

reports/validation_q1_p5_clean.pdf: python-results/validation_q1_p5.pkl python-results
	$(PYTHON) $(PLOT_VAL_ROC) python-results/validation_q1_p5.pkl reports/validation_q1_p5_clean.pdf

reports/roc_cv_q3_p4_clean.pdf: python-results/roc_cv_q3_p4.pkl python-results
	$(PYTHON) $(PLOT_CV_ROC) python-results/roc_cv_q1_p5.pkl

reports/validation_q3_p4_clean.pdf: python-results/validation_q3_p4.pkl python-results
	$(PYTHON) $(PLOT_VAL_ROC) python-results/validation_q3_p4.pkl reports/validation_q3_p4_clean.pdf

# PDF reports recipes
reports/roc_%.pdf: python-results/roc_%.pkl reports
	$(PYTHON) $(PLOT_CV_ROC) $< $@ t

reports/validation_%.pdf: python-results/validation_%.pkl reports
	$(PYTHON) $(PLOT_VAL_ROC) $< $@ t

# Directory creation recipes
clean-data python-results reports:
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
