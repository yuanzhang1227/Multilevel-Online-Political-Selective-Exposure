library(ggplot2)
library(tidyverse) 
library(FactoMineR) 
library(factoextra) 
library(scales) 
library(ggrepel) 
library(broom) 
library(kableExtra) 
library(betareg) 
library(VGAM)


### Run Negative Binomial Regression 
my_data$Overlap_scale <- my_data$Overlap * 10
forward_stepwise <- function(data, response, criterion = "BIC") {
  predictors <- c(pca_continuous_vars, pca_categorical_vars)
  selected <- NULL
  best_model <- vglm(formula(paste(response, "~ 1")), data = data, family = posnegbinomial())
  best_variables <- list()
  best_criteria <- list()
  all_variables <- list()
  all_criteria <- list()
  
  while(length(predictors) > 0) {
    models <- list()
    for (i in seq_along(predictors)) {
      formula_str <- paste(response, "~", paste(c(selected, predictors[i]), collapse=" + "))
      model <- vglm(as.formula(formula_str), data = data, family = posnegbinomial())
      models[[i]] <- model
    }
    
    criteria <- sapply(models, function(model) {
      if (criterion == "AIC") {
        return(AIC(model))
      } else if (criterion == "BIC") {
        return(BIC(model))
      } else if (criterion == "Adj-R2") {
        return(summary(model)$adj.r.squared)
      } else if (criterion == "Cp") {
        n <- length(model$residuals)
        k <- length(model$coefficients) - 1
        return((sum(model$residuals^2) / n) / (model$sigma^2) - n + 2 * k)
      } else if (criterion == "RSS") {
        return(sum(residuals(model)^2))
      } else {
        stop("Criterion not supported.")
      }
    })
    
    best_index <- which.min(criteria)
    best_criterion <- criteria[best_index]
    best_model <- models[[best_index]]
    best_variable <- predictors[best_index]
    ##store the results
    best_variables[[length(best_variables) + 1]] <- best_variable
    best_criteria[[length(best_criteria) + 1]] <- best_criterion
    all_variables[[length(all_variables) + 1]] <- predictors
    all_criteria[[best_variable]] <- criteria
    
    predictors <- setdiff(predictors, best_variable)
    selected <- c(selected, best_variable)
  }
  
  return(list(best_variables = best_variables,
              best_criteria = best_criteria,
              all_variables = all_variables,
              all_criteria = all_criteria))
}

# Perform forward stepwise selection
results <- forward_stepwise(my_data, response = "Overlap_scale", criterion = "BIC")

# Initialize a list to store BIC values for each variable
model_bic_values <- list()

# Initialize the null model
selected <- character(0)

# Iterate over each variable in results$best_variables
for (variable in results$best_variables) {
  selected <- c(selected, variable)
  selected_formula <- paste(selected, collapse = " + ")
  formula_str <- paste("Overlap_scale", "~", selected_formula)
  model <- vglm(formula_str, data = my_data, family = posnegbinomial())
  bic <- BIC(model)
  model_bic_values[[variable]] <- bic
}

# BIC Data
bic_df <- data.frame(
  Variable = factor(names(model_bic_values), levels = names(model_bic_values)),
  Value = as.numeric(unlist(model_bic_values)),
  Data.Type = "BICs of Model Justification"
)

# Criteria Data
data <- results$all_criteria
df <- map_df(data, ~data.frame(Value = .x), .id = "Variable")
df$Variable <- factor(df$Variable, levels = names(data))
df$Data.Type <- "BICs of Stepwise Variable Selection"

# Combine the data frames
combined_df <- bind_rows(bic_df, df)


plot1 <- ggplot(combined_df, aes(x = Variable, y = Value)) +
  geom_line(data = combined_df %>% filter(Data.Type == "BICs of Model Justification"), aes(group = 1), color = "red") +
  geom_point(alpha = 0.5, color = "darkblue") +
  labs(x = "Variable", y = "BIC Value", title = "Selection of Independent Variables for Community Overlap (Level 4)") +
  facet_wrap(~ Data.Type, scales = "free_y") +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust = 1, size = 15),
        axis.text.y = element_text(size = 15),
        axis.title.x = element_text(size = 20),
        axis.title.y = element_text(size = 20),
        strip.text = element_text(size = 20),
        plot.title = element_text(size = 25, hjust = 0.5))

### Run Beta Regression - Identity Diversity (with nans)
N <- nrow(my_data)
s <- 0.5
my_data$adjusted_proportion <- (my_data$Label_diversity_with_nans * (N - 1) + s) / N
forward_stepwise <- function(data, response, criterion = "BIC") {
  predictors <- c(pca_continuous_vars, pca_categorical_vars)
  selected <- NULL
  best_variables <- list()
  best_criteria <- list()
  all_variables <- list()
  all_criteria <- list()
  
  while(length(predictors) > 0) {
    if (length(best_variables) > 169) {
      break
    }
    models <- list()
    for (i in seq_along(predictors)) {
      formula_str <- paste(response, "~", paste(c(selected, predictors[i]), collapse=" + "))
      model <- betareg(as.formula(formula_str), data = data)
      models[[i]] <- model
    }
    
    criteria <- sapply(models, function(model) {
      if (criterion == "AIC") {
        return(AIC(model))
      } else if (criterion == "BIC") {
        return(BIC(model))
      } else if (criterion == "Adj-R2") {
        return(summary(model)$adj.r.squared)
      } else if (criterion == "Cp") {
        n <- length(model$residuals)
        k <- length(model$coefficients) - 1
        return((sum(model$residuals^2) / n) / (model$sigma^2) - n + 2 * k)
      } else if (criterion == "RSS") {
        return(sum(residuals(model)^2))
      } else {
        stop("Criterion not supported.")
      }
    })
    
    criteria[criteria == -Inf] <- NA
    if (all(is.na(criteria))) {
      cat("All values in criteria are NA, skipping selection.\n")
      break
    } else {
      best_index <- which.min(criteria)
      best_criterion <- criteria[best_index]
      best_model <- models[[best_index]]
      best_variable <- predictors[best_index]
      best_variables[[length(best_variables) + 1]] <- best_variable
      best_criteria[[length(best_criteria) + 1]] <- best_criterion
      all_variables[[length(all_variables) + 1]] <- predictors
      all_criteria[[best_variable]] <- criteria[!is.na(criteria)]
      
      predictors <- setdiff(predictors, best_variable)
      selected <- c(selected, best_variable)
    }
  }
  return(list(best_variables = best_variables,
              best_criteria = best_criteria,
              all_variables = all_variables,
              all_criteria = all_criteria))
}

# Perform forward stepwise selection
results <- forward_stepwise(my_data, response = "adjusted_proportion", criterion = "BIC")

# Initialize a list to store BIC values for each variable
model_bic_values <- list()

# Initialize the null model
selected <- character(0)

# Iterate over each variable in results$best_variables
for (variable in results$best_variables) {
  selected <- c(selected, variable)
  selected_formula <- paste(selected, collapse = " + ")
  formula_str <- paste("adjusted_proportion", "~", selected_formula)
  model <- betareg(formula_str, data = my_data)
  bic <- BIC(model)
  model_bic_values[[variable]] <- bic
}

# BIC Data
bic_df <- data.frame(
  Variable = factor(names(model_bic_values), levels = names(model_bic_values)),
  Value = as.numeric(unlist(model_bic_values)),
  Data.Type = "BICs of Model Justification"
)

# Criteria Data
data <- results$all_criteria
df <- map_df(data, ~data.frame(Value = .x), .id = "Variable")
df$Variable <- factor(df$Variable, levels = names(data))
df$Data.Type <- "BICs of Stepwise Variable Selection"

# Combine the data frames
combined_df <- bind_rows(bic_df, df)

plot2 <- ggplot(combined_df, aes(x = Variable, y = Value)) +
  geom_line(data = combined_df %>% filter(Data.Type == "BICs of Model Justification"), aes(group = 1), color = "red") +
  geom_point(alpha = 0.5, color = "darkblue") +
  labs(x = "Variable", y = "BIC Value", title = "Selection of Independent Variables for Identity Diversity with Nans (Level 4)") +
  facet_wrap(~ Data.Type, scales = "free_y") +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust = 1, size = 15),
        axis.text.y = element_text(size = 15),
        axis.title.x = element_text(size = 20),
        axis.title.y = element_text(size = 20),
        strip.text = element_text(size = 20),
        plot.title = element_text(size = 25, hjust = 0.5))



### Run Beta Regression - Identity Diversity (without nans)
N <- nrow(my_data)
s <- 0.5
my_data$adjusted_proportion <- (my_data$Label_diversity_without_nans * (N - 1) + s) / N
forward_stepwise <- function(data, response, criterion = "BIC") {
  predictors <- c(pca_continuous_vars, pca_categorical_vars) 
  selected <- NULL
  best_variables <- list()
  best_criteria <- list()
  all_variables <- list()
  all_criteria <- list()
  
  while(length(predictors) > 0) {
    if (length(best_variables) > 169) {
      break
    }
    models <- list()
    for (i in seq_along(predictors)) {
      formula_str <- paste(response, "~", paste(c(selected, predictors[i]), collapse=" + "))
      model <- betareg(as.formula(formula_str), data = data)
      models[[i]] <- model
    }
    
    criteria <- sapply(models, function(model) {
      if (criterion == "AIC") {
        return(AIC(model))
      } else if (criterion == "BIC") {
        return(BIC(model))
      } else if (criterion == "Adj-R2") {
        return(summary(model)$adj.r.squared)
      } else if (criterion == "Cp") {
        n <- length(model$residuals)
        k <- length(model$coefficients) - 1
        return((sum(model$residuals^2) / n) / (model$sigma^2) - n + 2 * k)
      } else if (criterion == "RSS") {
        return(sum(residuals(model)^2))
      } else {
        stop("Criterion not supported.")
      }
    })
    
    criteria[criteria == -Inf] <- NA
    if (all(is.na(criteria))) {
      cat("All values in criteria are NA, skipping selection.\n")
      break
    } else {
      best_index <- which.min(criteria)
      best_criterion <- criteria[best_index]
      best_model <- models[[best_index]]
      best_variable <- predictors[best_index]
      best_variables[[length(best_variables) + 1]] <- best_variable
      best_criteria[[length(best_criteria) + 1]] <- best_criterion
      all_variables[[length(all_variables) + 1]] <- predictors
      all_criteria[[best_variable]] <- criteria[!is.na(criteria)]
      
      predictors <- setdiff(predictors, best_variable)
      selected <- c(selected, best_variable)
      print(length(best_variables))
    }
  }
  return(list(best_variables = best_variables,
              best_criteria = best_criteria,
              all_variables = all_variables,
              all_criteria = all_criteria))
}

# Perform forward stepwise selection
results <- forward_stepwise(my_data, response = "adjusted_proportion", criterion = "BIC")

# Initialize a list to store BIC values for each variable
model_bic_values <- list()

# Initialize the null model
selected <- character(0)

# Iterate over each variable in results$best_variables
for (variable in results$best_variables) {
  selected <- c(selected, variable)
  selected_formula <- paste(selected, collapse = " + ")
  formula_str <- paste("adjusted_proportion", "~", selected_formula)
  model <- betareg(formula_str, data = my_data)
  bic <- BIC(model)
  model_bic_values[[variable]] <- bic
}

# BIC Data
bic_df <- data.frame(
  Variable = factor(names(model_bic_values), levels = names(model_bic_values)),
  Value = as.numeric(unlist(model_bic_values)),
  Data.Type = "BICs of Model Justification"
)

# Criteria Data
data <- results$all_criteria
df <- map_df(data, ~data.frame(Value = .x), .id = "Variable")
df$Variable <- factor(df$Variable, levels = names(data))
df$Data.Type <- "BICs of Stepwise Variable Selection"

# Combine the data frames
combined_df <- bind_rows(bic_df, df)

plot3 <- ggplot(combined_df, aes(x = Variable, y = Value)) +
  geom_line(data = combined_df %>% filter(Data.Type == "BICs of Model Justification"), aes(group = 1), color = "red") +
  geom_point(alpha = 0.5, color = "darkblue") +
  labs(x = "Variable", y = "BIC Value", title = "Selection of Independent Variables for Identity Diversity without Nans (Level 4)") +
  facet_wrap(~ Data.Type, scales = "free_y") +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust = 1, size = 15),
        axis.text.y = element_text(size = 15),
        axis.title.x = element_text(size = 20),
        axis.title.y = element_text(size = 20),
        strip.text = element_text(size = 20),
        plot.title = element_text(size = 25, hjust = 0.5))


### Run Beta Regression - Information Diversity
N <- nrow(my_data)
s <- 0.5
my_data$adjusted_proportion <- (my_data$Domain_diversity * (N - 1) + s) / N
forward_stepwise <- function(data, response, criterion = "BIC") {
  predictors <- c(pca_continuous_vars, pca_categorical_vars)
  selected <- NULL
  best_variables <- list()
  best_criteria <- list()
  all_variables <- list()
  all_criteria <- list()
  
  while(length(predictors) > 0) {
    if (length(best_variables) > 169) {
      break
    }
    models <- list()
    for (i in seq_along(predictors)) {
      formula_str <- paste(response, "~", paste(c(selected, predictors[i]), collapse=" + "))
      model <- betareg(as.formula(formula_str), data = data)
      models[[i]] <- model
    }
    
    criteria <- sapply(models, function(model) {
      if (criterion == "AIC") {
        return(AIC(model))
      } else if (criterion == "BIC") {
        return(BIC(model))
      } else if (criterion == "Adj-R2") {
        return(summary(model)$adj.r.squared)
      } else if (criterion == "Cp") {
        n <- length(model$residuals)
        k <- length(model$coefficients) - 1
        return((sum(model$residuals^2) / n) / (model$sigma^2) - n + 2 * k)
      } else if (criterion == "RSS") {
        return(sum(residuals(model)^2))
      } else {
        stop("Criterion not supported.")
      }
    })
    
    criteria[criteria == -Inf] <- NA
    if (all(is.na(criteria))) {
      cat("All values in criteria are NA, skipping selection.\n")
      break
    } else {
      best_index <- which.min(criteria)
      best_criterion <- criteria[best_index]
      best_model <- models[[best_index]]
      best_variable <- predictors[best_index]
      best_variables[[length(best_variables) + 1]] <- best_variable
      best_criteria[[length(best_criteria) + 1]] <- best_criterion
      all_variables[[length(all_variables) + 1]] <- predictors
      all_criteria[[best_variable]] <- criteria[!is.na(criteria)]
      
      predictors <- setdiff(predictors, best_variable)
      selected <- c(selected, best_variable)
      print(length(best_variables))
    }
  }
  return(list(best_variables = best_variables,
              best_criteria = best_criteria,
              all_variables = all_variables,
              all_criteria = all_criteria))
}

# Perform forward stepwise selection
results <- forward_stepwise(my_data, response = "adjusted_proportion", criterion = "BIC")

# Initialize a list to store BIC values for each variable
model_bic_values <- list()

# Initialize the null model
selected <- character(0)

# Iterate over each variable in results$best_variables
for (variable in results$best_variables) {
  selected <- c(selected, variable)
  selected_formula <- paste(selected, collapse = " + ")
  formula_str <- paste("adjusted_proportion", "~", selected_formula)
  model <- betareg(formula_str, data = my_data)
  bic <- BIC(model)
  model_bic_values[[variable]] <- bic
}

# BIC Data
bic_df <- data.frame(
  Variable = factor(names(model_bic_values), levels = names(model_bic_values)),
  Value = as.numeric(unlist(model_bic_values)),
  Data.Type = "BICs of Model Justification"
)

# Criteria Data
data <- results$all_criteria
df <- map_df(data, ~data.frame(Value = .x), .id = "Variable")
df$Variable <- factor(df$Variable, levels = names(data))
df$Data.Type <- "BICs of Stepwise Variable Selection"

# Combine the data frames
combined_df <- bind_rows(bic_df, df)


plot4 <- ggplot(combined_df, aes(x = Variable, y = Value)) +
  geom_line(data = combined_df %>% filter(Data.Type == "BICs of Model Justification"), aes(group = 1), color = "red") +
  geom_point(alpha = 0.5, color = "darkblue") +
  labs(x = "Variable", y = "BIC Value", title = "Selection of Independent Variables for Information Diversity (Level 4)") +
  facet_wrap(~ Data.Type, scales = "free_y") +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust = 1, size = 15),
        axis.text.y = element_text(size = 15),
        axis.title.x = element_text(size = 20),
        axis.title.y = element_text(size = 20),
        strip.text = element_text(size = 20),
        plot.title = element_text(size = 25, hjust = 0.5))


### Run Beta Regression - Structural Isolation
N <- nrow(my_data)
s <- 0.5
my_data$adjusted_proportion <- (my_data$Normalized_cut * (N - 1) + s) / N
forward_stepwise <- function(data, response, criterion = "BIC") {
  predictors <- c(pca_continuous_vars, pca_categorical_vars) 
  selected <- NULL
  best_variables <- list()
  best_criteria <- list()
  all_variables <- list()
  all_criteria <- list()
  
  while(length(predictors) > 0) {
    if (length(best_variables) > 169) {
      break
    }
    models <- list()
    for (i in seq_along(predictors)) {
      formula_str <- paste(response, "~", paste(c(selected, predictors[i]), collapse=" + "))
      model <- betareg(as.formula(formula_str), data = data)
      models[[i]] <- model
    }
    
    criteria <- sapply(models, function(model) {
      if (criterion == "AIC") {
        return(AIC(model))
      } else if (criterion == "BIC") {
        return(BIC(model))
      } else if (criterion == "Adj-R2") {
        return(summary(model)$adj.r.squared)
      } else if (criterion == "Cp") {
        n <- length(model$residuals)
        k <- length(model$coefficients) - 1
        return((sum(model$residuals^2) / n) / (model$sigma^2) - n + 2 * k)
      } else if (criterion == "RSS") {
        return(sum(residuals(model)^2))
      } else {
        stop("Criterion not supported.")
      }
    })
    
    criteria[criteria == -Inf] <- NA
    if (all(is.na(criteria))) {
      cat("All values in criteria are NA, skipping selection.\n")
      break
    } else {
      best_index <- which.min(criteria)
      best_criterion <- criteria[best_index]
      best_model <- models[[best_index]]
      best_variable <- predictors[best_index]
      best_variables[[length(best_variables) + 1]] <- best_variable
      best_criteria[[length(best_criteria) + 1]] <- best_criterion
      all_variables[[length(all_variables) + 1]] <- predictors
      all_criteria[[best_variable]] <- criteria[!is.na(criteria)]
      
      predictors <- setdiff(predictors, best_variable)
      selected <- c(selected, best_variable)
      print(length(best_variables))
    }
  }
  return(list(best_variables = best_variables,
              best_criteria = best_criteria,
              all_variables = all_variables,
              all_criteria = all_criteria))
}

# Perform forward stepwise selection
results <- forward_stepwise(my_data, response = "adjusted_proportion", criterion = "BIC")

# Initialize a list to store BIC values for each variable
model_bic_values <- list()

# Initialize the null model
selected <- character(0)

# Iterate over each variable in results$best_variables
for (variable in results$best_variables) {
  selected <- c(selected, variable)
  selected_formula <- paste(selected, collapse = " + ")
  formula_str <- paste("adjusted_proportion", "~", selected_formula)
  model <- betareg(formula_str, data = my_data)
  bic <- BIC(model)
  model_bic_values[[variable]] <- bic
}

# BIC Data
bic_df <- data.frame(
  Variable = factor(names(model_bic_values), levels = names(model_bic_values)),
  Value = as.numeric(unlist(model_bic_values)),
  Data.Type = "BICs of Model Justification"
)

# Criteria Data
data <- results$all_criteria
df <- map_df(data, ~data.frame(Value = .x), .id = "Variable")
df$Variable <- factor(df$Variable, levels = names(data))
df$Data.Type <- "BICs of Stepwise Variable Selection"

# Combine the data frames
combined_df <- bind_rows(bic_df, df)


plot5 <- ggplot(combined_df, aes(x = Variable, y = Value)) +
  geom_line(data = combined_df %>% filter(Data.Type == "BICs of Model Justification"), aes(group = 1), color = "red") +
  geom_point(alpha = 0.5, color = "darkblue") +
  labs(x = "Variable", y = "BIC Value", title = "Selection of Independent Variables for Structural Isolation (Level 4)") +
  facet_wrap(~ Data.Type, scales = "free_y") +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust = 1, size = 15),
        axis.text.y = element_text(size = 15),
        axis.title.x = element_text(size = 20),
        axis.title.y = element_text(size = 20),
        strip.text = element_text(size = 20),
        plot.title = element_text(size = 25, hjust = 0.5))


### Run Beta Regression - Connectivity Inequality
N <- nrow(my_data)
s <- 0.5
my_data$adjusted_proportion <- (my_data$Gini * (N - 1) + s) / N
forward_stepwise <- function(data, response, criterion = "BIC") {
  predictors <- c(pca_continuous_vars, pca_categorical_vars) #names(data)[1:(ncol(data)-7)]
  selected <- NULL
  best_variables <- list()
  best_criteria <- list()
  all_variables <- list()
  all_criteria <- list()
  
  while(length(predictors) > 0) {
    if (length(best_variables) > 169) {
      break
    }
    models <- list()
    for (i in seq_along(predictors)) {
      formula_str <- paste(response, "~", paste(c(selected, predictors[i]), collapse=" + "))
      model <- betareg(as.formula(formula_str), data = data)
      models[[i]] <- model
    }
    
    criteria <- sapply(models, function(model) {
      if (criterion == "AIC") {
        return(AIC(model))
      } else if (criterion == "BIC") {
        return(BIC(model))
      } else if (criterion == "Adj-R2") {
        return(summary(model)$adj.r.squared)
      } else if (criterion == "Cp") {
        n <- length(model$residuals)
        k <- length(model$coefficients) - 1
        return((sum(model$residuals^2) / n) / (model$sigma^2) - n + 2 * k)
      } else if (criterion == "RSS") {
        return(sum(residuals(model)^2))
      } else {
        stop("Criterion not supported.")
      }
    })
    
    criteria[criteria == -Inf] <- NA
    if (all(is.na(criteria))) {
      cat("All values in criteria are NA, skipping selection.\n")
      break
    } else {
      best_index <- which.min(criteria)
      best_criterion <- criteria[best_index]
      best_model <- models[[best_index]]
      best_variable <- predictors[best_index]
      best_variables[[length(best_variables) + 1]] <- best_variable
      best_criteria[[length(best_criteria) + 1]] <- best_criterion
      all_variables[[length(all_variables) + 1]] <- predictors
      all_criteria[[best_variable]] <- criteria[!is.na(criteria)]
      
      predictors <- setdiff(predictors, best_variable)
      selected <- c(selected, best_variable)
      print(length(best_variables))
    }
  }
  return(list(best_variables = best_variables,
              best_criteria = best_criteria,
              all_variables = all_variables,
              all_criteria = all_criteria))
}

# Perform forward stepwise selection
results <- forward_stepwise(my_data, response = "adjusted_proportion", criterion = "BIC")

# Initialize a list to store BIC values for each variable
model_bic_values <- list()

# Initialize the null model
selected <- character(0)

# Iterate over each variable in results$best_variables
for (variable in results$best_variables) {
  selected <- c(selected, variable)
  selected_formula <- paste(selected, collapse = " + ")
  formula_str <- paste("adjusted_proportion", "~", selected_formula)
  model <- betareg(formula_str, data = my_data)
  bic <- BIC(model)
  model_bic_values[[variable]] <- bic
}

# BIC Data
bic_df <- data.frame(
  Variable = factor(names(model_bic_values), levels = names(model_bic_values)),
  Value = as.numeric(unlist(model_bic_values)),
  Data.Type = "BICs of Model Justification"
)

# Criteria Data
data <- results$all_criteria
df <- map_df(data, ~data.frame(Value = .x), .id = "Variable")
df$Variable <- factor(df$Variable, levels = names(data))
df$Data.Type <- "BICs of Stepwise Variable Selection"

# Combine the data frames
combined_df <- bind_rows(bic_df, df)


plot6 <- ggplot(combined_df, aes(x = Variable, y = Value)) +
  geom_line(data = combined_df %>% filter(Data.Type == "BICs of Model Justification"), aes(group = 1), color = "red") +
  geom_point(alpha = 0.5, color = "darkblue") +
  labs(x = "Variable", y = "BIC Value", title = "Selection of Independent Variables for Connectivity Inequality (Level 4)") +
  facet_wrap(~ Data.Type, scales = "free_y") +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust = 1, size = 15),
        axis.text.y = element_text(size = 15),
        axis.title.x = element_text(size = 20),
        axis.title.y = element_text(size = 20),
        strip.text = element_text(size = 20),
        plot.title = element_text(size = 25, hjust = 0.5))

# save the plot for each level
combined_bic <- (plot1 + plot2) / (plot3 + plot4) / (plot5 + plot6) +
  plot_layout(guides = 'collect') &
  theme(plot.margin = margin(10, 10, 10, 10, "mm"))
ggsave("/Users/yuazhan/Downloads/SI_Fig.13_BIC_L4.png", combined_bic, width = 30, height = 25, units = "in", dpi = 300)

# replaced by "SI_Fig.10_BIC_L1.png", "SI_Fig.11_BIC_L2.png", "SI_Fig.12_BIC_L3.png"
