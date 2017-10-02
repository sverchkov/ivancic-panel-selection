# Makefile for R data processing
RCMD = rscript

data-clean/training.rds : data-clean/features.v2.rds intermediates
	$(RCMD) expand_training.R

data-clean/features.v2.rds : data-clean
	$(RCMD) raw_to_clean_v2.R

data-clean :
	mkdir data-clean

intermediates :
	mkdir intermediates