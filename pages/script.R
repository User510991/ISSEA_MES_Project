# script.R
args <- commandArgs(trailingOnly = TRUE)

# Load required library
# If you're using a specific library for the model, ensure it's loaded. For example:
# library(randomForest)  # If the model is from randomForest

# Step 1: Download and load the model from the URL
url <- "https://example.com/your_model.rds"  # Replace with actual URL of the model
temp_model_file <- tempfile(fileext = ".rds")
download.file(url, temp_model_file)
model <- readRDS(temp_model_file)

# Step 2: Create initial data (replace this with your actual data)
data <- data.frame(
  var1 = c(10, 20, 30),
  var2 = c(5, 10, 15)
)

# Step 3: Make initial predictions using the loaded model
predictions_initial <- predict(model, newdata = data)

# Step 4: Save initial predictions to a CSV file
write.csv(predictions_initial, "predictions_initial.csv", row.names = FALSE)

# Step 5: Modify the data (e.g., change var1 values)
data_modified <- data
data_modified$var1 <- c(15, 25, 35)  # Change var1 values

# Step 6: Make new predictions with the modified data
predictions_modified <- predict(model, newdata = data_modified)

# Step 7: Save modified predictions to a CSV file
write.csv(predictions_modified, "predictions_modified.csv", row.names = FALSE)

# Print messages to confirm
cat("Initial predictions saved to predictions_initial.csv\n")
cat("Modified predictions saved to predictions_modified.csv\n")
