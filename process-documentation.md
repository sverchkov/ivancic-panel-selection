# Process Documentation

1. Files from Dr. Melanie Ivancic are in `Raw_Data`.
Using the Excel Macro in that folder, CSV files in `Raw_Data_csv` are created.

2. Using `R/raw_to_clean.R` create `.rds` files and `.csv` file for `Clean_Data_csv`

3. Using `R/update_training_data.R` create the training set
(Note: it uses `Training_Data/Old/training_data.csv`, never delete that).

4. Using `R/extractValidationData.R` create the validation set

5. Using `R/RunMeanImputations.R` create mean-imputed feature tables

6. Using `R/(Training|Validation)_to_Question_#.R` create question-specific feature tables

7. Run analyses using `python/q#(cv|val).py`
