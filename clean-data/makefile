# Makefile for R data processing, creating files for python
RCMD = rscript ../R/rds-to-questions-cli.R
TRAINING = ../R/data-clean/training.rds
VALIDATION = ../R/data-clean/validation.rds

all: plain validation

plain: q1-training.csv q2-training.csv q3-training.csv q1-validation.csv q2-validation.csv q3-validation.csv

imputed: q1-training-imputed.csv q2-training-imputed.csv q3-training-imputed.csv q1-validation-imputed.csv q2-validation-imputed.csv q3-validation-imputed.csv

q1-training-imputed.csv : $(TRAINING)
	$(RCMD) $@ q1 training impute $(TRAINING)

q2-training-imputed.csv : $(TRAINING)
	$(RCMD) $@ q2 training impute $(TRAINING)

q3-training-imputed.csv : $(TRAINING)
	$(RCMD) $@ q3 training impute $(TRAINING)

q1-validation-imputed.csv : $(VALIDATION) $(TRAINING)
	$(RCMD) $@ q1 validation impute $(TRAINING) $(VALIDATION)

q2-validation-imputed.csv : $(VALIDATION) $(TRAINING)
	$(RCMD) $@ q2 validation impute $(TRAINING) $(VALIDATION)

q3-validation-imputed.csv : $(VALIDATION) $(TRAINING)
	$(RCMD) $@ q3 validation impute $(TRAINING) $(VALIDATION)

q1-training.csv : $(TRAINING)
	$(RCMD) $@ q1 training none $(TRAINING)

q2-training.csv : $(TRAINING)
	$(RCMD) $@ q2 training none $(TRAINING)

q3-training.csv : $(TRAINING)
	$(RCMD) $@ q3 training none $(TRAINING)

q1-validation.csv : $(VALIDATION)
	$(RCMD) $@ q1 validation none $(VALIDATION)

q2-validation.csv : $(VALIDATION)
	$(RCMD) $@ q2 validation none $(VALIDATION)

q3-validation.csv : $(VALIDATION)
	$(RCMD) $@ q3 validation none $(VALIDATION)
