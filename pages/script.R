# script.R
args <- commandArgs(trailingOnly = TRUE)

# Load required library
# If you're using a specific library for the model, ensure it's loaded. For example:
# library(randomForest)  # If the model is from randomForest
library(moments)
library(urca)
library(readxl)
library(tseries)
library(ggplot2)
library(FinTS)
library(caschrono)
library(nortest)
library(lmtest)
library(strucchange)
library(vars)
library(dynlm)
library(tsDyn)
library(dLagM)
library(dynamac)
library(TSstudio)  
library(ARDL)
library(TSA)   
library(car)
library(nardl)
library(CPAT)   
library(systemfit)
library(AER)
library(foreign)
library(vars)
library(xtable)
library(stargazer)
library(timeSeries)
library(Hmisc)
library(texreg)   
library(tsDyn)
library(dynamac)
library(forecast)




# Step 1: Download and load the model from the URL
url <- "https://raw.githubusercontent.com/User510991/ISSEA_MES_Project/refs/heads/Essaies/model_3sls.RData"  # Replace with actual URL of the model
temp_model_file <- tempfile(fileext = ".rData")
download.file(url, temp_model_file)
model <- readRDS(temp_model_file)

data_init <- read.csv('data_new_init.csv')

# Step 3: Make initial predictions using the loaded model
predictions_initial <- predict(model,newdata = data_init,interval = "confidence")

# Step 4: Save initial predictions to a CSV file
write.csv(predictions_initial, "predictions_initial.csv", row.names = FALSE)


data_modified <- read.csv('data_new.csv')

# Step 6: Make new predictions with the modified data
predictions_modified <- predict(model, newdata = data_modified, interval = "confidence")

# Step 7: Save modified predictions to a CSV file
write.csv(predictions_modified, "predictions_modified.csv", row.names = FALSE)
# 6. Calcul de l'impact (différence entre les prédictions initiales et modifiées)
impact <- predictions_modified - predictions_initial
write.csv(impact, "impact.csv", row.names = FALSE)
