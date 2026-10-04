EF5560 2026 ML assignment
Submission instructions updated: 20 September 2026
Data release: 19 September 2026 (unchanged)

Read EF5560_ML_Investment_Project_2026.pdf for the five questions and submission requirements.

Data:
  project_data_handout_2026.csv and .xlsx contain the same 20,800 rows.
  Use either format, not both.
  data_dictionary_2026.csv lists the 17 predictors and other fields.
  HSI_80_asset_map_2026.csv identifies the 80 company labels.

All numeric observations are simulated. Signal values are dimensionless.
The outcome is already matched to its forecast row.
Prediction target: ret_next_week - rf_weekly.

Submission: one team of up to three submits three files with the same lead ID.
  EF5560_leadstudentid_report.pdf - Q1-Q5; searchable text and tables.
  EF5560_leadstudentid.csv - private-period portfolio weights.
  EF5560_leadstudentid_code.zip - source code appendix for verification.

  report_outline_2026.txt is an optional starting point for the report.
  Do not submit the outline or the input data.
  Code ZIP: at most 10 MB; R/Python scripts or notebooks and helper source
  files only. Do not include data or installed packages. No separate README
  is required. Code length and programming style are not graded.
  Name the main script/notebook, software/package versions, and random seeds
  at the end of the report,
  together with a brief statement of any AI tools used and your own checks.

Weight file:
  Read portfolio_weight_rules_2026.txt for constraints, examples, and format.
  Fill submission_template_2026.csv with your 156 weekly weight vectors.
  equal_weight_example_2026.csv is a valid formatting example.
  Run one checker:
    python check_submission_2026.py EF5560_12345678.csv
    Rscript check_submission_2026.R EF5560_12345678.csv
  Keep the checker and template together. Python needs no extra packages.

This release replaces earlier assignment data. Use the files in this folder together.
