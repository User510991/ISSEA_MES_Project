import rpy2.robjects as ro
from rpy2.robjects.packages import importr
from rpy2.robjects import pandas2ri

# Activer la conversion entre pandas et R
pandas2ri.activate()

# Charger le modèle R (modèle préenregistré)
ro.r('load("model_fit.RData")')  # Charge l'objet appelé `fit` contenant le modèle

# Extraire les variables explicatives et instrumentales
ro.r('''
extract_variables <- function(model) {
    result <- list(
        explicatives = model$eq[[1]]$terms,  # Variables explicatives
        instrumentales = model$inst         # Variables instrumentales
    )
    return(result)
}
''')

# Appeler la fonction R
extract_variables = ro.globalenv["extract_variables"]
variables = extract_variables(ro.globalenv["fit"])

# Convertir les résultats en Python
explicatives = list(variables[0])
instrumentales = list(variables[1])

# Afficher les résultats
print("Variables explicatives :")
print(explicatives)

print("\nVariables instrumentales :")
print(instrumentales)
