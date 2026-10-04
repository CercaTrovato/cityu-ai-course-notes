# EF5560 2026 ML Investment Project submission checker
#
# Put this script, submission_template_2026.csv, and your weight file in the
# same folder.  Change only the file name below, or pass a file name when
# running: Rscript check_submission_2026.R EF5560_12345678.csv

args <- commandArgs(trailingOnly = TRUE)
submission_file <- if (length(args) >= 1) args[1] else "EF5560_leadstudentid.csv"
script_arg <- grep("^--file=", commandArgs(), value = TRUE)
script_dir <- if (length(script_arg)) dirname(normalizePath(sub("^--file=", "", script_arg[1]))) else "."
template_file <- file.path(script_dir, "submission_template_2026.csv")
tolerance <- 1e-6
weight_cap <- 0.10

fail <- function(message) {
  cat("FAIL:", message, "\n")
  quit(status = 1)
}

if (!file.exists(submission_file)) fail(paste("Cannot find", submission_file))
if (!file.exists(template_file)) fail(paste("Cannot find", template_file))

submission <- read.csv(submission_file, check.names = FALSE, stringsAsFactors = FALSE)
template <- read.csv(template_file, check.names = FALSE, stringsAsFactors = FALSE)

if (nrow(submission) != 156) fail("The file must contain exactly 156 weekly rows.")
if (ncol(submission) != 81) fail("The file must contain forecast_date plus 80 ticker columns.")
if (!identical(names(submission), names(template))) {
  fail("Column names and order must match submission_template_2026.csv exactly.")
}
if (!identical(as.character(submission$forecast_date), as.character(template$forecast_date))) {
  fail("forecast_date values or their order do not match the template.")
}

weights <- submission[, -1, drop = FALSE]
numeric_columns <- vapply(weights, is.numeric, logical(1))
if (!all(numeric_columns)) fail("Every weight column must be numeric.")

weight_matrix <- as.matrix(weights)
if (any(!is.finite(weight_matrix))) fail("Weights contain NA, NaN, or infinite values.")
if (any(weight_matrix < -tolerance)) fail("Weights must be non-negative.")
if (any(weight_matrix > weight_cap + tolerance)) fail("No stock weight may exceed 10%.")

row_sums <- rowSums(weight_matrix)
if (any(abs(row_sums - 1) > tolerance)) {
  bad_rows <- which(abs(row_sums - 1) > tolerance)
  fail(paste("Some rows do not sum to 1. First bad row:", bad_rows[1]))
}

cat("PASS: 156 dates and 80 ticker columns match the template.\n")
cat("PASS: all weights are finite, non-negative, and no greater than 10%.\n")
cat("PASS: every row sums to 100% within tolerance.\n")
cat("Your file is structurally ready to submit. This check does not evaluate performance.\n")
