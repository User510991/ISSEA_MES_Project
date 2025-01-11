# script.R
args <- commandArgs(trailingOnly = TRUE)


# Load required library
# Fonction pour installer un package s'il n'est pas installé
install_if_missing <- function(pkg) {
    if (!require(pkg, character.only = TRUE)) {
        install.packages(pkg)
    }
}

# Liste des packages nécessaires
#required_packages <- c("moments", "urca", "readxl", "tseries", "ggplot2", "FinTS", 
#                   "caschrono", "nortest", "lmtest", "strucchange", "vars", 
#                   "dynlm", "tsDyn", "dLagM", "dynamac", "TSstudio", "ARDL", 
#                   "TSA", "car", "nardl", "CPAT", "systemfit", "AER", "foreign", 
#                   "xtable", "stargazer", "timeSeries", "Hmisc", "texreg", "forecast")

# Installer tous les packages nécessaires
#sapply(required_packages, install_if_missing)

# If you're using a specific library for the model, ensure it's loaded. For example:
# library(randomForest)  # If the model is from randomForest
library(systemfit)




# Step 1: Download and load the model from the URL
url <- "https://raw.githubusercontent.com/User510991/ISSEA_MES_Project/refs/heads/Essaies/model_3sls.RData"  # Replace with actual URL of the model
temp_model_file <- tempfile(fileext = ".RData")
download.file(url, temp_model_file)
load(temp_model_file)

data_init <- read.csv('data_new_init.csv')

# Step 3: Make initial predictions using the loaded model
predictions_initial <- predict(modeleTCD,newdata = data_init,interval = "confidence")

# Step 4: Save initial predictions to a CSV file
write.csv(predictions_initial, "predictions_initial.csv", row.names = FALSE)


data_modified <- read.csv('data_new.csv')

# Step 6: Make new predictions with the modified data
predictions_modified <- predict(modeleTCD, newdata = data_modified, interval = "confidence")
print(dim(predictions_modified))
print(dim(predictions_initial))
# Step 7: Save modified predictions to a CSV file
write.csv(predictions_modified, "predictions_modified.csv", row.names = FALSE)
# 6. Calcul de l'impact (différence entre les prédictions initiales et modifiées)
impact <- predictions_modified - predictions_initial
write.csv(impact, "impact.csv", row.names = FALSE)
