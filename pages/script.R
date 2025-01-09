# script.R
args <- commandArgs(trailingOnly = TRUE)
x <- as.numeric(args[1])
# Load required library
# If you're using a specific library for the model, ensure it's loaded. For example:
# library(randomForest)  # If the model is from randomForest

# Step 1: Download and load the model from the URL
url <- "https://raw.githubusercontent.com/User510991/ISSEA_MES_Project/refs/heads/Essaies/model_3sls.RData"  # Replace with actual URL of the model
temp_model_file <- tempfile(fileext = ".rData")
download.file(url, temp_model_file)
model <- readRDS(temp_model_file)


# Step 3: Make initial predictions using the loaded model
predictions_initial <- predict(model, interval = "confidence", n.ahead = x)

# Step 4: Save initial predictions to a CSV file
write.csv(predictions_initial, "predictions_initial.csv", row.names = FALSE)

# Step 5: Modify the data (e.g., change var1 values)
# Step 1: Specify the URL for the modified data CSV
url_data <- "https://example.com/modified_data.csv"  # Replace with actual URL

# Step 2: Define a temporary file path to store the downloaded data
temp_data_file <- tempfile(fileext = ".csv")

# Step 3: Download the modified data CSV file
download.file(url_data, temp_data_file)

# Step 4: Load the modified data into R
data_modified <- read.csv(temp_data_file)

# Step 6: Make new predictions with the modified data
predictions_modified <- predict(model, newdata = data_modified, interval = "confidence", n.ahead = 10)

# Step 7: Save modified predictions to a CSV file
write.csv(predictions_modified, "predictions_modified.csv", row.names = FALSE)
# 6. Calcul de l'impact (différence entre les prédictions initiales et modifiées)
impact <- predictions_modified - predictions_initial
write.csv(impact, "impact.csv", row.names = FALSE)
